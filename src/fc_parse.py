import re
from fc_token import Token,TokenType as tt
from fc_ast import *

def parse(tokens) ->  (int,str,Program):
    """
    Build parse tree / AST from the tokens.
    """
    tokens.reverse()
    token = tokens.pop()
    if not token.is_type(tt.PROGRAM):
        msg = f"Error in {build_parse_tree.__qualname__}. Expected {tt.PROGRAM=}, got {token=}"
        return False,msg,None
    
    token = tokens.pop()
    if not token.is_type(tt.IDENTIFIER):
        msg = f"Error in {build_parse_tree.__qualname__}. Expected {tt.IDENTIFIER}, got {token=}"
        return False,msg,None
    
    program = Program(value=token.get_value())
    retcode,msg = _parse_program(program=program,tokens=tokens)
    
    return retcode,msg,program

def _parse_program(program:Program,tokens:list) -> (int, str):
    # GRAMMAR:
    # <program> ::= PROGRAM <identifier> LBRACE <statement_list> <function_list> RBRACE 
    
    token = tokens.pop()
    if not token.is_type(tt.LBRACE):
        return 0,f"Error in {_parse_program.__qualname__}. Expected {tt.LBRACE=}, got {token=}"
    
    token = tokens.pop()
    while(not token.is_type(tt.RBRACE)):
        retcode = False
        msg = None
        match(token.get_type()):
            case tt.FUNC:
                # token = tokens.pop()
                fun = Function(position=token.get_position())
                program.add_function(function=fun)
                retcode,msg = _parse_function(function=fun,
                                              tokens=tokens)
                print(f"at parse program, <- parse function: {msg}")
                    
            case tt.IDENTIFIER:
                stmt = Statement(position=token.get_position(),
                                 value=token.get_value())
                program.add_statement(statement=stmt)
                retcode,msg = _parse_statement(statement=stmt,
                                               tokens=tokens)
                
            case _:
                retcode = False   
                msg = f"Error in {_parse_program.__qualname__}. \
                    Expected {tt.FUNC=} or {tt.IDENTIFIER=}, \
                    got {token.get_type()=}"    
             
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
        return False,f"Error in {_parse_function.__qualname__}. Expected {tt.IDENTIFIER=}, got {token=}"
    else:
        function.set_value(token.get_value())
        
    print(f"At _parse_function: {function.get_value()}")

    token = tokens.pop()
    if not token.is_type(tt.LPAREN):
        return False,f"Error in {_parse_function.__qualname__}. Expected {tt.LPAREN=}, got {token=}"
    
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
                return False,f"Error in {_parse_function.__qualname__}. Expected {tt.LPAREN=}, got {token=}"
    
    token = tokens.pop()
    if not token.is_type(tt.LBRACE):
        return False,f"Error in {_parse_function.__qualname__}. Expected {tt.LBRACE=}, got {token=}"
    
    token = tokens.pop()
    while(not token.is_type(tt.RBRACE)):
        retcode = False
        msg = ""
        statement = Statement(position=token.get_value())
        
        match(token.get_type()):
            case tt.IDENTIFIER:
                statement.set_value(token.get_value())
                retcode,msg = _parse_statement(statement=statement,tokens=tokens)
            
            case tt.RETURN_STATEMENT:
                statement.set_statement_type(StatementType.RETURN)
                expression = Expression()
                statement.set_statement(expression)
                retcode,msg = _parse_expression(expression=expression,tokens=tokens) 
                print(f"At parse function <- parse expression: {msg}")
                
            case _:
                msg = f"Error in {_parse_function.__qualname__}. Invalid start of statement, got {token=}"
                
        if retcode == False:
            return retcode,msg
        else:
            function.add_statement(statement)
            token = tokens.pop()
    
    return True,"ok"

def _parse_statement(statement:Statement,tokens:list) -> (int,str):       
    # <statement> ::= <assignment_statement> | <function_call> SEMICOLON
    #   <assignment_statement> ::= <identifier> <operator> <expression> SEMICOLON 
    #   <function_call> ::= <identifier> LPAREN <argument_list> RPAREN              
    print("At _parse_statement")
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
            function_call = FunctionCall()
            statement.set_statement(function_call)
            _parse_function_call(function_call,tokens)
            token = tokens.pop()
            if not token.is_type(tt.SEMICOLON):
                msg = f"Error at {_parse_statement.__qualname__}. Expected SEMICOLON after function call, got {token}"
                return False,msg

        case _:
            return False, f"No match in parse statement: {token=}"

    return True,"ok"
# TODO: refactor
def _parse_expression(expression:Expression,tokens:list)->(int,str):
    # <expression> ::= <term>
    #             | <expression> <operator> <term>
    #             | <term> <operator> <expression>  
    #             | <function_call>
    #             | LPAREN <expression> RPAREN
    assert(expression.get_operator() == None)
    assert(expression.get_expression_right() == None)

    token = None
    if tokens:
        token = tokens.pop()
    else:
        return False,f"Error at {_parse_expression.__qualname__}. Expression not closed"
    
    if token.is_type(tt.SEMICOLON):
        return True, "ok"

    match(token.get_type()):
        case tt.LPAREN:
            sub_expression = Expression(sub_exp=True)
            sub_tokens = []
            while(not token.is_type(tt.RPAREN)):
                if tokens:
                    token = tokens.pop()
                    sub_tokens.append(token)
                else:
                    msg = f"Error at {_parse_expression.__qualname__}: Out of tokens when parsing sub-expression."
                    return False,msg
            sub_tokens.pop() # Drop RPAREN
            sub_tokens.append(Token(t_type=tt.SEMICOLON,value=';',position=token.get_position()))
            sub_tokens.reverse()
            
            retcode,msg = _parse_expression(expression=sub_expression,tokens=sub_tokens)
            if retcode:
                expression.set_expression_left(sub_expression)
                setter = expression.set_operator
            else:
                return retcode,msg
            
        case tt.OPERATOR:
            retcode,op_type = Operator.get_type(token.get_value())
            if retcode:
                expression.set_operator(op_type)
                expand_exp = Expression()
                expression.set_expression_right(expand_exp)
                return _parse_expression(expression=expand_exp,tokens=tokens)
            else:
                msg = f"Error at {_parse_expression.__qualname__}: No matching operator in {token}"
                return False, msg
        
        case tt.IDENTIFIER:  # Terminal or function_call 
            if tokens[-1].is_type(tt.LPAREN):
                # statement.set_statement_type(StatementType.FUNCTION_CALL)
                function_call = FunctionCall()
                # statement.set_statement(function_call)
                expression.set_expression_left(function_call)
                _parse_function_call(function_call,tokens)
            else:
                expression.set_expression_left(
                    Terminal(terminal_type=TerminalType.IDENTIFIER,
                             value=token.get_value(),
                             position=token.get_position()))
        
        case tt.INTEGER:
            expression.set_expression_left(Terminal(terminal_type=TerminalType.INTEGER,
                                                    value=token.get_value(),
                                                    position=token.get_position()))
        
        case tt.FLOAT:
            expression.set_expression_left(Terminal(terminal_type=TerminalType.INTEGER,
                                                    value=token.get_value(),
                                                    position=token.get_position()))
        
        case tt.STRING_LITERAL:
            expression.set_expression_left(Terminal(terminal_type=TerminalType.STRING,
                                                    value=token.get_value(),
                                                    position=token.get_position()))
        case _:
            msg = f"Error at {_parse_expression.__qualname__}: No matching type in {token}"
            return False,msg

    print("End of parse_expression.")
    return _parse_expression(expression=expression,tokens=tokens)

def _parse_term():
    # <term> ::= <integer>
    #          | <identifier>
    #          | <string_literal>
    pass

def _parse_function_call(fcall:FunctionCall,tokens:list):
    # <function_call> ::= <identifier> 
    #                 LPAREN <argument_list> RPAREN  
    token = tokens.pop()
    while(not token.is_type(tt.RPAREN)): # TODO function call
        print(f"Parameter: {token}")
        token = tokens.pop()