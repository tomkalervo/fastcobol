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
    program = None
    tokens.reverse()
    token = tokens.pop()
    if token.isProgram():
        program = TokenNode(token)
    else:
        print("Error, incorrect Program declaration")
    
    return program

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