import re
from fc_token import Token,TokenType
from fc_ast import Node,ProgramNode,FunctionNode,StatementNode

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
    
    def parse_next(func,_list:list,token:Token,Node_t:'Node') -> None:
        node = Node_t(parent=tree_node,
                      value=token.get_value(),
                      position=token.get_position())
        retcode,msg,node = func(node=node,
                            tokens=tokens)
        if retcode == False:
            return retcode,msg,None
        else:
            _list.append(node)
            
    while(not token.is_type(TokenType.RBRACE)):
        match(token.get_type()):
            case TokenType.FUNC:
                token = tokens.pop()
                if not token.is_type(TokenType.IDENTIFIER):
                    return 0,f"Expected {TokenType.IDENTIFIER=}, got {token=}",None

                parse_next(func=_parse_function,
                           _list=function_list,
                           token=token,
                           Node_t=FunctionNode)
                    
            case TokenType.IDENTIFIER:
                parse_next(func=_parse_statement,
                           _list=statement_list,
                           token=token,
                           Node_t=StatementNode)

            case _:
                return 0,f"Expected {TokenType.FUNC=} or {TokenType.IDENTIFIER=}, got {token.get_type()=}",None        

        token = tokens.pop()
            
    return 1,"ok",tree_node

def _parse_function(node:Node,tokens:list) -> (int,str, Node):    
    # <function> ::= FUNC <identifier> 
    #            LPAREN <parameter_list> RPAREN 
    #            LBRACE <statement_list> <return_statement> RBRACE    
    
    token = tokens.pop()
    if not token.is_type(TokenType.LPAREN):
        return 0,f"Expected {TokenType.LPAREN=}, got {token=}",None
    
    print("Parameterlist:")
    print(f"{token=}")
    token = tokens.pop()
    while(not token.is_type(TokenType.RPAREN)):
        print(f"{token=}")
        token = tokens.pop()
    print(f"{token=}")

    token = tokens.pop()
    if not token.is_type(TokenType.LBRACE):
        return 0,f"Expected {TokenType.LBRACE=}, got {token=}",None
    
    print("statementlist:")
    print(f"{token=}")
    token = tokens.pop()
    while(not token.is_type(TokenType.RBRACE)):
        print(f"{token=}")
        token = tokens.pop()
    print(f"{token=}")
    
    # match(token.get_type()):
    #     case "operator":
    #         print(f"Got assignment_statement {token=}")
    #         while(not token.is_type("SEMICOLON")):
    #             token = tokens.pop()
    #     case "LPAREN":
    #         print(f"Got function call {token=}")
    #         while(not token.is_type("RPAREN")):
    #             token = tokens.pop()
    #     case _:
    #         print(f"bad match in parse statement {token=}")
                
    #     token = tokens.pop()

    return 1,"ok", Node(position=token.get_position,value="function")

def _parse_statement(node: Node,tokens:list) -> (int,str, Node):       
    # <statement> ::= <assignment_statement> | <function_call> SEMICOLON
    #   <assignment_statement> ::= <identifier> <operator> <expression> SEMICOLON 
    #   <function_call> ::= <identifier> LPAREN <argument_list> RPAREN  
    
    token = tokens.pop()
    match(token.get_type()):
        case TokenType.OPERATOR:
            print(f"Got assignment statement: {TokenType.OPERATOR=} with {token=}")
            while(not token.is_type(TokenType.SEMICOLON)):
                token = tokens.pop()
        case TokenType.LPAREN:
            print(f"Got function call: {token=}")
            while(not token.is_type(TokenType.RPAREN)):
                token = tokens.pop()
        case _:
            print(f"bad match in parse statement {token=}")
            return 0, "Error", None

    return 1,"ok", Node(position=token.get_position,value="statement")