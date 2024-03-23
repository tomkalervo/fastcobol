"""
Token Module

This module provides classes and utilities for tokenizing the fastcobol programming language source code.

Tokens are fundamental building blocks in the parsing process, 
representing individual units of meaning in a program, 
such as keywords, identifiers, literals, and punctuation symbols.

Classes:
- Token: Represents a single token with a type, value, and position in the source code.
- Tokenizer: Takes fastcobol code as a text string and break it down into tokens.

Utilities:
- token_regex: A dictionary mapping token names to regular expressions.
- compiled_regex: A compiled version of token_regex.

"""
import re
from enum import Enum,auto

STOP_TOKEN = ['{','(',')','}',',',';','=','-','+','*','/']
QUOTE_TOKEN = ['"','\'']
# Compile regular expressions
# compiled_regex = {token_name: re.compile(regex) for token_name, regex in token_regex.items()}
class TokenType(Enum):
    PROGRAM = auto()
    FUNC = auto()
    RETURN_STATEMENT = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    STRING_LITERAL = auto()
    OPERATOR = auto()
    ASSIGN_STATEMENT = auto()
    FUNC_CALL = auto()
    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self._name_)
    
def get_regex() -> dict:
    tt = TokenType
    return {
        tt.PROGRAM: r"PROGRAM",
        tt.FUNC: r"FUNC",
        tt.RETURN_STATEMENT: r"RETURN",
        tt.LPAREN: r"\(",
        tt.RPAREN: r"\)",
        tt.LBRACE : r"\{",
        tt.RBRACE : r"\}",
        tt.SEMICOLON: r";",
        tt.COMMA: r",",
        tt.IDENTIFIER: r"[a-zA-Z_][a-zA-Z0-9_]*",
        tt.INTEGER: r"\d+",
        tt.STRING_LITERAL: r"\".*?\"",
        tt.OPERATOR: r"\+|-|\*|\/|=", 
        tt.ASSIGN_STATEMENT: r"[a-zA-Z_][a-zA-Z0-9_]*=", 
        tt.FUNC_CALL: r"[a-zA-Z_][a-zA-Z0-9_]*\(",
    }

class Token:
    def __init__(self, t_type, value, position):
        self._type = t_type
        self._value = value
        self._position = position
        
    def get_type(self) -> str:
        return self._type
    
    def get_value(self) -> str:
        return self._value
    
    def get_position(self) -> str:
        return self._position
    
    def __repr__(self):
        return f"Token({self._type}, {self._value}, {self._position})"
    
    def is_type(self,t_type) -> bool:
        return self._type == t_type
     
class Tokenizer:
    def __init__(self,string:str) -> None:
        self._string = string
        self._end = len(self._string)
        self._idx = 0
        self._current_row = 1 # 1-index rows
        self._token_regex = get_regex()
        
    def get_next_token(self) -> 'Token':
        if self._idx == self._end:
            return (0,None)
        else:
            pass
        #discard whitespace, recursive to handle eof
        while self._string[self._idx].isspace():
            if self._string[self._idx] == '\n':
                self._current_row += 1
            else:
                pass
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
        
        token_type = None
        for token, regex in self._token_regex.items():
            if re.match(regex, token_me):
                token_type = token
                break
            else:
                pass
                
        self._idx = idx_stop
        if token_type:
            return (1,Token(token_type,token_me,self._current_row))
        else:
            return (2,Token("No token match",token_me,self._current_row))

def tokenize(program_string,verbose=True) -> (int, str, list()):
    """
    Tokenize the input program string using regular expressions.
    """
    # Tokenize the program string
    tokens = []
    tkz = Tokenizer(program_string)
        
    rcode, my_token = tkz.get_next_token()
    if verbose:
        print(f"{rcode=},{my_token=}")
    tokens.append(my_token)

    while rcode == True:
        rcode, my_token = tkz.get_next_token()
        if verbose:
            print(f"{rcode=},{my_token=}")
        if rcode == 1:
            tokens.append(my_token)
        elif rcode == 2:
            if verbose:
                print('error parsing')
                print(f'{my_token=}')
            return (0,f'Error tokenize {my_token=}',None)

    return (1,'ok',tokens)