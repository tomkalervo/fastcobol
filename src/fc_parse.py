import re
from fc_token import Token,TokenType
from fc_ast import *

def build_parse_tree(tokens) ->  Node:
    """
    Build the parse tree or AST from the tokens.
    """
    tokens.reverse()
    token = tokens.pop()
    if not token.is_type(TokenType.PROGRAM):
        print(f"Expected {TokenType.PROGRAM=}, got {token=}")
        return None
    
    token = tokens.pop()
    if not token.is_type(TokenType.IDENTIFIER):
        return 0,f"Expected {TokenType.IDENTIFIER}, got {token=}",None
    
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
    if not token.is_type(TokenType.LBRACE):
        return 0,f"Expected {TokenType.LBRACE=}, got {token=}",None
    
    token = tokens.pop()
    function_list = []
    statement_list = []
    
    def parse_next(func,_list:list,token:Token,Node_t:'Node') -> (int,str):
        node = Node_t(parent=tree_node,
                      value=token.get_value(),
                      position=token.get_position())
        _list.append(node)
        return func(node=node, tokens=tokens)
            
    while(not token.is_type(TokenType.RBRACE)):
        retcode = False
        msg = None
        match(token.get_type()):
            case TokenType.FUNC:
                token = tokens.pop()
                if not token.is_type(TokenType.IDENTIFIER):
                    return False,f"Expected {TokenType.IDENTIFIER=}, got {token=}",None

                retcode,msg = parse_next(func=_parse_function,
                                         _list=function_list,
                                         token=token,
                                         Node_t=FunctionNode)
                    
            case TokenType.IDENTIFIER:
                retcode,msg = parse_next(func=_parse_statement,
                                         _list=statement_list,
                                         token=token,
                                         Node_t=StatementNode)
                
            case _:
                retcode,msg = False,f"Expected {TokenType.FUNC=} or {TokenType.IDENTIFIER=}, got {token.get_type()=}"    
                    
        if retcode == False:
            return False,msg,None
        
        token = tokens.pop()
            
    return True,"ok",tree_node

def _parse_function(node:Node,tokens:list) -> (int,str):    
    # <function> ::= FUNC <identifier> 
    #            LPAREN <parameter_list> RPAREN 
    #            LBRACE <statement_list> <return_statement> RBRACE    
    
    token = tokens.pop()
    if not token.is_type(TokenType.LPAREN):
        return False,f"Expected {TokenType.LPAREN=}, got {token=}"
    
    token = tokens.pop()
    while(not token.is_type(TokenType.RPAREN)):
        match(token.get_type()):
            case TokenType.IDENTIFIER:
                parameter = IdentifierNode(value=token.get_value(),
                                        position=token.get_position(),
                                        parent=node)
                node.add_parameter(parameter)
                token = tokens.pop()
                
            case TokenType.COMMA:
                token = tokens.pop()
                
            case _:
                return False,f"Expected {TokenType.LPAREN=}, got {token=}"
            
    # print("Parameterlist:")
    # for p in node.get_parameter_list():
    #     print(f"{p.get_value()=}")
    
    token = tokens.pop()
    if not token.is_type(TokenType.LBRACE):
        return False,f"Expected {TokenType.LBRACE=}, got {token=}"
    
    token = tokens.pop()
    while(not token.is_type(TokenType.RBRACE)):
        print(f"Parse {token=},{token.get_type()=}")
        match(token.get_type()):
            case TokenType.IDENTIFIER:
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
                    
            case TokenType.RETURN_STATEMENT:
                return_statement = ReturnNode(parent=node,
                                              value=token.get_value(),
                                              position=token.get_position())
                #TODO _parse_expression()
                node.add_return_statement(return_statement)
                
                while(not token.is_type(TokenType.SEMICOLON)):
                    token = tokens.pop()

                token = tokens.pop()

            case _:
                return False,f"Expected {TokenType.IDENTIFIER=}, got {token=}"
            
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
        case TokenType.ASSIGNMENT:
            while(not token.is_type(TokenType.SEMICOLON)): # TODO expression
                token = tokens.pop()
        case TokenType.LPAREN:
            while(not token.is_type(TokenType.SEMICOLON)): # TODO function call
                token = tokens.pop()
        case _:
            return 0, f"No match in parse statement: {token=}"

    return 1,"ok"