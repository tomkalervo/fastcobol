import re
from token import Token, TokenNode, compiled_regex, token_regex, Tokenizer

def tokenize(program_string) -> list():
    """
    Tokenize the input program string using regular expressions.
    """
    # Tokenize the program string
    tokens = []
    tkz = Tokenizer(program_string)
        
    rcode, my_token = tkz.get_next_token()
    print(f"{rcode=},{my_token=}")
    tokens.append(my_token)

    while rcode == True:
        rcode, my_token = tkz.get_next_token()
        print(f"{rcode=},{my_token=}")
        if rcode == 1:
            tokens.append(my_token)
        elif rcode == 2:
            print('error parsing')
            print(f'{my_token=}')
            break

    return tokens

def build_parse_tree(tokens) -> TokenNode:
    """
    Build the parse tree or AST from the tokens.
    """
    tokens.reverse()
    token = tokens.pop()
    if not token.is_type("PROGRAM"):
        print(f"Expected PROGRAM, got {token=}")
        return None
        
    retcode,msg,program = _parse_program(
        TokenNode(t_type=token.get_type(),position=token.get_position()),
        tokens)
    
    if retcode == False:
        print(msg)
        return None
    
    return program

def _parse_program(tree_node:TokenNode,tokens:list) -> (int, str, TokenNode):
    # Structure of program: identifier { content }
    iden = tokens.pop()
    if not iden.is_type("identifier"):
        return 0,f"Expected identifier, got {iden=}",None
    tree_node.set_value(iden.get_value())
    
    next_token = tokens.pop()
    if not next_token.is_type("LBRACE"):
        return 0,f"Expected LBRACE, got {next_token=}",None
    
    next_token = tokens.pop()
    while(not next_token.is_type("RBRACE")):
        retcode,msg,node = _parse_new_node(tree_node,next_token,tokens)
        if retcode == False:
            return retcode,msg,None
        else:
            tree_node.add_child(node)
            next_token = tokens.pop()
            
    return 1,"ok",tree_node

def _parse_new_node(parent_node,token,tokens) -> (int,str,TokenNode):
    # is new node function or statement
    match(token.get_type()):
        case "FUNC":
            print(f"FUNC, {token=}")
        case "identifier":
            print(f"identifier, {token=}")
        case _:
            print(f"no match, {token=}")

    return 1,"ok",TokenNode(t_type=token.get_type,position=token.get_position)


# Example program string
example_program = """
PROGRAM example
{
    FUNC add(x, y)
    {
        RETURN x + y;
    }

    FUNC main
    {
        result = add(3, 4);
        12ss = y;
        print "The result is: " + result;
    }
}
"""

# Tokenize the program string
tokens = tokenize(example_program)
for t in tokens:
    print(t)
# Build the parse tree or AST from the tokens
parse_tree = build_parse_tree(tokens)

# Print the parse tree (or AST) to visualize the structure
# print(parse_tree)

# t = Tokenizer(example_program)
# for row, match in t:
#     print(f"{row}:\t{match=}")