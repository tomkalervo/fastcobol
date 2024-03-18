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
import re

def get_match(string:str) -> str:
    for token, regex in token_regex.items():
        if re.match(regex, string):
            return token
    return None

token_regex = {
    "PROGRAM": r"PROGRAM",
    "FUNC": r"FUNC",
    "LPAREN": r"\(",
    "RPAREN": r"\)",
    "LBRACE" : r"\{",
    "RBRACE" : r"\}",
    "SEMICOLON": r";",
    "COMMA": r",",
    "identifier": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "integer": r"\d+",
    "string_literal": r"\".*?\"",
    "operator": r"\+|-|\*|\/|=",  # Add more operators as needed
    "RETURN": r"RETURN",
    "print_statement": r"print",
    "assignment_statement": r"[a-zA-Z_][a-zA-Z0-9_]*=",  # Assuming identifiers for assignment
    "function_call": r"[a-zA-Z_][a-zA-Z0-9_]*\(",  # Assuming function names consist of letters and underscores
}
STOP_TOKEN = ['{','(',')','}',',',';','=','-','+','*','/']
QUOTE_TOKEN = ['"','\'']

# Compile regular expressions
compiled_regex = {token_name: re.compile(regex) for token_name, regex in token_regex.items()}

class Token:
    def __init__(self, t_type, value, position):
        self._type = t_type
        self._value = value
        self._position = position

    def __repr__(self):
        return f"Token({self._type}, {self._value}, {self._position})"
    
    def isProgram(self) -> bool:
        return self.t_type == "PROGRAM"

class TokenNode:
    def __init__(self, token):
        self._token = token
        self._children = []
        
    def __repr__(self):
        children_repr = ', '.join(repr(child) for child in self._children)
        return f"TokenNode({repr(self._token)}, children=[{children_repr}])"
        
class Tokenizer:
    def __init__(self, string):
        self._string = string
        self._iter = re.finditer('|'.join(token_regex.values()), string)
        self._end = len(self._string)
        self._idx = 0
        self._current_row = 0
        
    def get_next_token(self) -> 'Token':
        if self._idx == self._end:
            return (0,None)
        
        #discard whitespace, recursive to handle eof
        while self._string[self._idx].isspace():
            self._idx += 1
            return self.get_next_token()
        
        idx_start = self._idx
        idx_stop = idx_start + 1

        if self._string[self._idx] in STOP_TOKEN:
            pass
        elif self._string[self._idx] in QUOTE_TOKEN:
            # parse string
            qt = QUOTE_TOKEN.index(self._string[self._idx])
            while self._string[idx_stop] != QUOTE_TOKEN[qt]:
                idx_stop += 1
            idx_stop += 1
        else:
            while self._string[idx_stop] not in STOP_TOKEN and not self._string[idx_stop].isspace():
                idx_stop += 1
            
        token_me = self._string[idx_start:idx_stop]
        token_type = get_match(token_me)
        self._idx = idx_stop
        if token_type:
            return (1,Token(token_type,token_me,(idx_start,idx_stop)))
        else:
            return (2,Token("No token match",token_me,(idx_start,idx_stop)))
            
    def __iter__(self):
        return self

    def __next__(self):
        match = next(self._iter)
        end = match.end()
        self._current_row += self._string.count('\n', self._idx, end)
        self._idx = end
        return (self._current_row, match)
