

import re
from token import Token, TokenNode, compiled_regex, token_regex

def tokenize(program_string):
    """
    Tokenize the input program string using regular expressions.
    """
    # Tokenize the program string
    tokens = []

    # Extract pattern strings from compiled regex objects
    regex_patterns = list(token_regex.values())

    # Create a combined regex pattern
    combined_regex = '|'.join(regex_patterns)

    # Iterate over each token in the program string
    for line_number, line in enumerate(program_string.split('\n')):
        for match in re.finditer(combined_regex, line):
            #print(f"{match=},{match.group()=},{line_number=}")
            # Find the token type corresponding to the matched pattern
            token_type = next(key for key, value in compiled_regex.items() if value.match(match.group()))
            tokens.append(Token(token_type, match.group(), (line_number, match.start() + 1)))

    return tokens

def build_parse_tree(tokens):
    """
    Build the parse tree or AST from the tokens.
    """
    # TODO

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
        print "The result is: " + result;
    }
}
"""

# Tokenize the program string
tokens = tokenize(example_program)
for t in tokens:
    print(t)
# Build the parse tree or AST from the tokens
# parse_tree = build_parse_tree(tokens)

# Print the parse tree (or AST) to visualize the structure
# print(parse_tree)
