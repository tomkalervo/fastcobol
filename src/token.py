"""
Token Module

This module provides classes and utilities for tokenizing the fastcobol programming language source code.

Tokens are fundamental building blocks in the parsing process, 
representing individual units of meaning in a program, 
such as keywords, identifiers, literals, and punctuation symbols.

Classes:
- Token: Represents a single token with a type, value, and position in the source code.
- TokenNode: Represents a node in a token-based abstract syntax tree (AST).

Utilities:
- token_regex: A dictionary mapping token names to regular expressions.
- compiled_regex: A compiled version of token_regex.

"""

class Token:
    def __init__(self, type_, value, position):
        self.type = type_
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.position})"

class TokenNode:
    def __init__(self, token):
        self.token = token
        self.children = []
        
    def __repr__(self):
        children_repr = ', '.join(repr(child) for child in self.children)
        return f"TokenNode({repr(self.token)}, children=[{children_repr}])"
    
token_regex = {
    "PROGRAM": r"PROGRAM",
    "FUNC": r"FUNC",
    "LPAREN": r"\(",
    "RPAREN": r"\)",
    "SEMICOLON": r";",
    "COMMA": r",",
    "identifier": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "integer": r"\d+",
    "string_literal": r"\".*?\"",
    "operator": r"\+|-|\*|\/",  # Add more operators as needed
    "print": r"print",
    "RETURN": r"RETURN",
    "print_statement": r"print",
    "assignment_statement": r"[a-zA-Z_][a-zA-Z0-9_]*=",  # Assuming identifiers for assignment
    "function_call": r"[a-zA-Z_][a-zA-Z0-9_]*\(",  # Assuming function names consist of letters and underscores
}

# Compile regular expressions
import re
compiled_regex = {token_name: re.compile(regex) for token_name, regex in token_regex.items()}
