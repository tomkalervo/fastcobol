from objects import *

VARIABLE = [
    'u_int',
    'int',
    'string'
]
FUNCTION = [
    'print'
]
USER_FUNCTION = r'\b[a-zA-Z0-9]+\s*\('
ERROR = 0
OK = 1

def map_it(text: str) -> (int,str):
    if not text:
        return ERROR, 'Empty text'
    docs = []
    line_i = 0
    lines = text.splitlines()
    lines_len = len(lines)
    # Check that Program is declared and enclosed
    while(lines[line_i].startswith('Program') != True):
        if len(lines[line_i]) == 0:
            continue
        elif lines[line_i] == '*':
            docs.append(Comment(lines[line_i]))
        else:
            return ERROR, 'Incorrect Program declaration'
        
        line_i += 1
        if line_i >= lines_len:
            return ERROR, 'Missing Program start-statement'

    program_statement = lines[line_i].split()
    if(len(program_statement) != 3 or program_statement[2] != '{'):
        return ERROR, "Incorrect Program declaration statement"
    
    prog = Program(name=program_statement[1])
    
    line_i += 1
    prog_start = line_i
    bracket = 1
    while(bracket > 0):
        if line_i > lines_len:
            return ERROR, 'Missing Program end-statement'
        
        bracket += lines[line_i].count('{')
        bracket -= lines[line_i].count('}')
        line_i += 1

    return_code,prog = parse_program(program=prog,lines_of_code=lines[prog_start:line_i-1])
    
    print(f"Map it completed with return code={return_code}")
    if return_code == ERROR:
        return ERROR, 'er'
    print(prog)
    for i,code in enumerate(prog.code):
        print(f"{i}:\t{code}")
        
    return OK, 'ok'

def parse_program(program:Program,lines_of_code:list) -> Program:
    return_code,code,data = parse_line([],[],lines_of_code,0,len(lines_of_code))
    if return_code == OK:
        program.code = code
        program.data = data
        return OK,program
    else:
        return ERROR,program

# Recursive function
def parse_line(code:list,data:list,lines_of_code:list,current_line:int,total_lines:int) -> (list,list):
    # Basecase
    if current_line == total_lines:
        return OK,code,data 
    
    expression = lines_of_code[current_line]
    print(expression)
    return_code,e_type,value = evaluate_expression(expression)
    print(f'{return_code},{e_type},{value}')
    if return_code == ERROR:
        ERROR,code,data
    
    # TODO
    # Handle return, library with function calls? v,f,uf
    
    current_line += 1
    # Recursive call
    return parse_line(code,data,lines_of_code,current_line,total_lines) 

def evaluate_expression(e):
    import re

    for v in VARIABLE:
        if e.strip().startswith(v):
            return OK,'v',v
        
    for f in FUNCTION:
        if e.strip().startswith(f):
            return OK,'f',f
        
    match = re.match(USER_FUNCTION, e)
    if match:
        return OK,'uf',match.group()

    return ERROR,'Incorrent line',e