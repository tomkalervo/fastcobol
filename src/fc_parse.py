import re
from fc_token import Token,TokenType as tt
from fc_ast import *

def build_parse_tree(tokens) ->  Node:
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
    
    retcode,msg,program = _parse_program(
        tree_node=ProgramNode(value=token.get_value(),
                              position=token.get_position()),
        tokens=tokens)
    
    if retcode == False:
        print(msg)
        return None
    
    return program

def _parse_program(tree_node:Node,tokens:list) -> (int, str,  Node):
    # GRAMMAR:
    # <program> ::= PROGRAM <identifier> LBRACE <statement_list> <function_list> RBRACE 
    
    token = tokens.pop()
    if not token.is_type(tt.LBRACE):
        return 0,f"Expected {tt.LBRACE=}, got {token=}",None
    
    token = tokens.pop()
    function_list = []
    statement_list = []
    
    def parse_next(func,_list:list,token:Token,Node_t:'Node') -> (int,str):
        node = Node_t(parent=tree_node,
                      value=token.get_value(),
                      position=token.get_position())
        _list.append(node)
        return func(node=node, tokens=tokens)
            
    while(not token.is_type(tt.RBRACE)):
        retcode = False
        msg = None
        match(token.get_type()):
            case tt.FUNC:
                token = tokens.pop()
                if not token.is_type(tt.IDENTIFIER):
                    return False,f"Expected {tt.IDENTIFIER=}, got {token=}",None

                retcode,msg = parse_next(func=_parse_function,
                                         _list=function_list,
                                         token=token,
                                         Node_t=FunctionNode)
                    
            case tt.IDENTIFIER:
                retcode,msg = parse_next(func=_parse_statement,
                                         _list=statement_list,
                                         token=token,
                                         Node_t=StatementNode)
                
            case _:
                retcode,msg = False,f"Expected {tt.FUNC=} or {tt.IDENTIFIER=}, got {token.get_type()=}"    
                    
        if retcode == False:
            return False,msg,None
        
        token = tokens.pop()
            
    return True,"ok",tree_node

def _parse_function(node:Node,tokens:list) -> (int,str):    
    # <function> ::= FUNC <identifier> 
    #            LPAREN <parameter_list> RPAREN 
    #            LBRACE <statement_list> <return_statement> RBRACE    
    
    token = tokens.pop()
    if not token.is_type(tt.LPAREN):
        return False,f"Expected {tt.LPAREN=}, got {token=}"
    
    token = tokens.pop()
    while(not token.is_type(tt.RPAREN)):
        match(token.get_type()):
            case tt.IDENTIFIER:
                parameter = IdentifierNode(value=token.get_value(),
                                        position=token.get_position(),
                                        parent=node)
                node.add_parameter(parameter)
                token = tokens.pop()
                
            case tt.COMMA:
                token = tokens.pop()
                
            case _:
                return False,f"Expected {tt.LPAREN=}, got {token=}"
            
    # print("Parameterlist:")
    # for p in node.get_parameter_list():
    #     print(f"{p.get_value()=}")
    
    token = tokens.pop()
    if not token.is_type(tt.LBRACE):
        return False,f"Expected {tt.LBRACE=}, got {token=}"
    
    token = tokens.pop()
    while(not token.is_type(tt.RBRACE)):
        # print(f"Parse {token=},{token.get_type()=}")
        match(token.get_type()):
            case tt.IDENTIFIER:
                statement = StatementNode(parent=node,
                                          value=token.get_value(),
                                          position=token.get_position())
                retcode,msg = _parse_statement(node=statement,
                                               tokens=tokens)
                if retcode == False:
                    return retcode,msg
                else:
                    node.add_statement(statement)
                    token = tokens.pop()
                    
            case tt.RETURN_STATEMENT:
                return_statement = ReturnNode(parent=node,
                                              value=token.get_value(),
                                              position=token.get_position())

                retcode,msg = _parse_expression(node=return_statement,
                                                tokens=tokens)
                if retcode == False:
                    return retcode,msg
                else:
                    node.add_return_statement(return_statement)
                    token = tokens.pop()

            case _:
                return False,f"Expected {tt.IDENTIFIER=}, got {token=}"
            
    # print("statementlist:")
    # for s in node.get_statement_list():
    #     print(f"{s.get_value()=}")
    
    return 1,"ok"

def _parse_statement(node: Node,tokens:list) -> (int,str):       
    # <statement> ::= <assignment_statement> | <function_call> SEMICOLON
    #   <assignment_statement> ::= <identifier> <operator> <expression> SEMICOLON 
    #   <function_call> ::= <identifier> LPAREN <argument_list> RPAREN  
    
    token = tokens.pop()
    match(token.get_type()):
        case tt.ASSIGNMENT:
            retcode,msg = _parse_expression(node=node,
                                            tokens=tokens)
            if retcode == False:
                return retcode,msg

        case tt.LPAREN:
            while(not token.is_type(tt.SEMICOLON)): # TODO function call
                token = tokens.pop()
        case _:
            return 0, f"No match in parse statement: {token=}"

    return 1,"ok"
# TODO: refactor
def _parse_expression(node:Node,tokens:list)->(int,str):
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

    def _parse_exp_list(tokens,expression_node):
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
                        exp = ExpressionNode(value=None,
                                             position=position,
                                             parent=expression_node)
                        _parse_exp_list(expression_list,exp)
                    else:
                        next_token = tokens.pop()
                        if next_token.is_type(tt.IDENTIFIER):
                            #function call
                            #TODO: parse argument_list
                            exp = FunctionCallNode(value=next_token.get_value(),
                                                position=position,
                                                parent=node,
                                                argument_list=expression_list)

                        elif next_token.is_type(tt.OPERATOR):
                            #expression
                            expression_node.set_operator(next_token)
                            exp = ExpressionNode(value=None,
                                                    position=position,
                                                    parent=expression_node)
                            _parse_exp_list(expression_list,exp)
                        else:
                            print(f"Error in get_expression. No match for {next_token=}")
                case tt.OPERATOR:
                    expression_node.set_operator(token)
                    exp = ExpressionNode(value=None,
                                         position=position,
                                         parent=expression_node)
                    _parse_exp_list(tokens,exp)
                case _:
                    exp = token
                    
            if expression_node.get_operator():
                expression_node.set_expression_right(exp)
                assert(len(tokens) == 0)
            else:
                expression_node.set_expression_left(exp)
                                                
    expression_node = ExpressionNode(value=None,position=token.get_position(),parent=node)
    # TODO: check if correct prior or add checks?
    _parse_exp_list(expression_token,expression_node)
    # print(f"{expression_node=}")
    
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