
STOP_TOKEN = ['{','(',')','}',',',';','=','-','+','*','/']
QUOTE_TOKEN = ['"','\'']

token_regex = {
    "PROGRAM": r"PROGRAM",
    "FUNC": r"FUNC",
    "RETURN": r"RETURN",
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
    "print_statement": r"print",
    "assignment_statement": r"[a-zA-Z_][a-zA-Z0-9_]*=",  # Assuming identifiers for assignment
    "function_call": r"[a-zA-Z_][a-zA-Z0-9_]*\(",  # Assuming function names consist of letters and underscores
}
# Compile regular expressions
compiled_regex = {token_name: re.compile(regex) for token_name, regex in token_regex.items()}
