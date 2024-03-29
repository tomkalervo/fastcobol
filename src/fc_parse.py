import re
from fc_token import Token,TokenType as tt
from fc_ast import *

def build_parse_tree(tokens) ->  Program:
    """
    Build the parse tree or AST from the tokens.
    """
    tokens.reverse()
    token = tokens.pop()
    if not token.is_type(tt.PROGRAM):
        print(f"Expected {tt.PROGRAM=}, got {token=}")
        return None
    
    token = tokens.pop()
    if not token.is_type(tt.IDENTIFIER):
        return 0,f"Expected {tt.IDENTIFIER}, got {token=}",None
    
    retcode,msg = _parse_program(
        program=Program(value=token.get_value()),
        tokens=tokens)
    
    if retcode == False:
        print(msg)
        return None
    
    return program

def _parse_program(program:Program,tokens:list) -> (int, str):
    # GRAMMAR:
    # <program> ::= PROGRAM <identifier> LBRACE <statement_list> <function_list> RBRACE 
    
    token = tokens.pop()
    if not token.is_type(tt.LBRACE):
        return 0,f"Expected {tt.LBRACE=}, got {token=}"
    
    token = tokens.pop()
    function_list = []
    statement_list = []
            
    while(not token.is_type(tt.RBRACE)):
        retcode = False
        msg = None
        match(token.get_type()):
            case tt.FUNC:
                token = tokens.pop()
                function = Function()
                retcode,msg = _parse_function(function=function,tokens=tokens)
                    
            case tt.IDENTIFIER:
                statement = Statement(value=token.get_value())
                retcode,msg = _parse_statement(statement=statement,tokens=tokens)
                
            case _:
                retcode,msg = False,f"Expected {tt.FUNC=} or {tt.IDENTIFIER=}, got {token.get_type()=}"    
                    
        if retcode == False:
            return False,msg
        
        token = tokens.pop()
            
    return True,"ok"

def _parse_function(function:Function,tokens:list) -> (int,str):    
    # <function> ::= FUNC <identifier> 
    #            LPAREN <parameter_list> RPAREN 
    #            LBRACE <statement_list> <return_statement> RBRACE    
    
    token = tokens.pop()
    if not token.is_type(tt.IDENTIFIER):
        return False,f"Expected {tt.IDENTIFIER=}, got {token=}"
    else:
        function.set_value(token.get_value())

    token = tokens.pop()
    if not token.is_type(tt.LPAREN):
        return False,f"Expected {tt.LPAREN=}, got {token=}"
    
    token = tokens.pop()
    while(not token.is_type(tt.RPAREN)):
        match(token.get_type()):
            case tt.IDENTIFIER:
                parameter = Terminal(value=token.get_value(),
                                        position=token.get_position(),
                                        terminal_type=TerminalType.IDENTIFIER)
                function.add_parameter(parameter)
                token = tokens.pop()
                
            case tt.COMMA:
                token = tokens.pop()
                
            case _:
                return False,f"Expected {tt.LPAREN=}, got {token=}"
    
    token = tokens.pop()
    if not token.is_type(tt.LBRACE):
        return False,f"Expected {tt.LBRACE=}, got {token=}"
    
    tokens.pop()
    while(not token.is_type(tt.RBRACE)):
        retcode = False
        msg = ""
        statement = Statement()
        
        match(token.get_type()):
            case tt.IDENTIFIER:
                statement.set_value(token.get_value())
                retcode,msg = _parse_statement(statement=statement,tokens=tokens)
            
            case tt.RETURN_STATEMENT:
                statement.set_statement_type(StatementType.RETURN)
                expression = Expression()
                statement.set_statement(expression)
                retcode,msg = _parse_expression(expression=expression,tokens=tokens) 
                           
        if retcode == False:
            return retcode,msg
        else:
            function.add_statement(statement)
            token = tokens.pop()
    
    return 1,"ok"

def _parse_statement(statement:Statement,tokens:list) -> (int,str):       
    # <statement> ::= <assignment_statement> | <function_call> SEMICOLON
    #   <assignment_statement> ::= <identifier> <operator> <expression> SEMICOLON 
    #   <function_call> ::= <identifier> LPAREN <argument_list> RPAREN              
            
    token = tokens.pop()
    match(token.get_type()):
        case tt.ASSIGNMENT:
            statement.set_statement_type(StatementType.ASSIGNMENT)
            expression = Expression()
            statement.set_statement(expression)
            retcode,msg = _parse_expression(expression=expression,
                                            tokens=tokens)
            if retcode == False:
                return retcode,msg

        case tt.LPAREN:
            statement.set_statement_type(StatementType.FUNCTION_CALL)
            function_call = FunctionCall(value=token.get_value())
            statement.set_statement(function_call)
            while(not token.is_type(tt.SEMICOLON)): # TODO function call
                token = tokens.pop()

        case _:
            return 0, f"No match in parse statement: {token=}"

    return 1,"ok"
# TODO: refactor
def _parse_expression(expression:Expression,tokens:list)->(int,str):
    # <expression> ::= <term>
    #             | <expression> <operator> <term>
    #             | <term> <operator> <expression>  
    #             | <function_call>
    #             | LPAREN <expression> RPAREN
    print("-"*10+"-> PARSE EXPR:")
    expression_token = []
    token = tokens.pop()
    row = token.get_position()
    while(not token.is_type(tt.SEMICOLON)):
        expression_token.append(token)
        if tokens:
            token = tokens.pop()
        else:
            return False,f"Invalid expression at row {row}: expression not closed"

    if not expression_token:
        return False,f"Invalid expression at row {row}: empty expression"

    print(f"{expression_token=}")

    def _parse_exp_list(tokens,expression):
        while(tokens):
            token = tokens.pop()
            position = token.get_position()
            match(token.get_type()):
                case tt.RPAREN:
                    expression_list = []
                    while(not token.is_type(tt.LPAREN)):
                        token = tokens.pop()
                        expression_list.append(token)
                    expression_list.pop()
                    expression_list.reverse()
                    if not tokens:
                        #expression
                        exp = Expression()
                        _parse_exp_list(expression_list,exp)
                    else:
                        next_token = tokens.pop()
                        if next_token.is_type(tt.IDENTIFIER):
                            #function call
                            #TODO: parse argument_list
                            exp = FunctionCall(value=next_token.get_value(),
                                                position=position,
                                                argument_list=expression_list)

                        elif next_token.is_type(tt.OPERATOR):
                            #expression
                            expression.set_operator(next_token)
                            exp = Expression()
                            _parse_exp_list(expression_list,exp)
                        else:
                            print(f"Error in get_expression. No match for {next_token=}")
                case tt.OPERATOR:
                    expression.set_operator(token)
                    exp = Expression()
                    _parse_exp_list(tokens,exp)
                case _:
                    exp = token
                    
            if expression.get_operator():
                expression.set_expression_right(exp)
                assert(len(tokens) == 0)
            else:
                expression.set_expression_left(exp)
                                                
    # expression = Expression()
    # TODO: check if correct prior or add checks?
    # _parse_exp_list(expression_token,expression)
    
    return True, "ok"

def _parse_term():
    # <term> ::= <integer>
    #          | <identifier>
    #          | <string_literal>
    pass

def _parse_function_call():
    # <function_call> ::= <identifier> 
    #                 LPAREN <argument_list> RPAREN  
    pass