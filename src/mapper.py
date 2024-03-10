from objects import *
VARIABLES = [
    'u_int',
    'int',
    'string'
]
FUNCTIONS = [
    'print'
]
USER_FUNCTION = r'\b[a-zA-Z0-9]+\s*\('
USER_VARIABLE = r'\b[a-zA-Z0-9]+\s*\='
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

    return_code = parse_program(program=prog,
                                lines_of_code=lines,
                                current_line=prog_start,
                                total_lines=line_i-1)
    
    print(f"Map it completed with return code={return_code}")
    if return_code == ERROR:
        return ERROR, 'er'
    print(prog)
    print("Procedures")
    for i,code in enumerate(prog.procedure):
        print(f"{i}:\t{code}")
    print("Data items")
    for v in prog.data:
        print(f"{v}:\t{prog.data[v]}")
    return OK, 'ok'

def parse_program(program:Program,
                  lines_of_code:list,
                  current_line:int,
                  total_lines:int) -> int:
    # Basecase
    if current_line == total_lines:
        return OK
    
    # Evaluate expression to prepare for builder
    expression = lines_of_code[current_line]
    return_code,e_type,value = evaluate_expression(expression)
    if return_code == ERROR:
        print(f'Error in evaluate_expression(): {e_type}. Expression value {value}')
        return ERROR
    
    # Parse expression and add to program
    return_code = parse_expression(program,e_type,lines_of_code,current_line,total_lines)
    if return_code == ERROR:
        return ERROR
        
    current_line += 1
    # Recursive call
    return parse_program(program=program,
                         lines_of_code=lines_of_code,
                         current_line=current_line,
                         total_lines=total_lines) 
# TODO:
# Three types of expressions: Operation, Function or Condition.
# Operation, in turn, can contain variable declaration.
# How many lines do the operation include? ; ?
# Function, in turn, can be defined by the user.
# How many lines do the function include? (){} ?
# Condition (if-else, evaluate-when): Future feature
def evaluate_expression(e):
    import re

    for v in VARIABLES:
        if e.strip().startswith(v):
            return OK,'v',v
    
    match = re.match(USER_VARIABLE, e)
    if match:
        return OK,'uv',match.group()
    
    for f in FUNCTIONS:
        if e.strip().startswith(f):
            return OK,'f',f
        
    match = re.match(USER_FUNCTION, e)
    if match:
        return OK,'uf',match.group()

    return ERROR,'Incorrent line',e

def parse_operation(process,expression:str) -> int:
    
    return OK

def get_user_variable(program:Program,lines:list,i:int,lines_len:int) -> int:

    return OK

def get_variable(program:Program,lines:list,i:int,lines_len:int) -> int:
    print(f'get_variable, {lines[i]}')
    expression = lines[i].strip().split()
    parts = len(expression)
    if parts < 4:
        return ERROR
    if expression[2] != '=':
        return ERROR
    # variable declaration
    ptype = expression[0]
    name = expression[1]
    if name not in program.data:
        v = Variable(ptype=ptype,name=name)
        if v.picType == None:
            return ERROR
        else:
            program.data[name] = v
        
    # VARIABLES expression / instance
    
    
    return OK
def get_function(program:Program,lines:list,i:int,lines_len:int) -> int:
    print(f'get_function, {lines[i]}')
    return OK
def get_user_function(program:Program,lines:list,i:int,lines_len:int) -> int:
    print(f'user_get_function, {lines[i]}')
    return OK

CODE_EXP = {
    'v':get_variable,
    'uv':get_user_variable,
    'f':get_function,
    'uf':get_user_function
}

def parse_expression(program:Program,e_type:str,lines:list,i:int,lines_len:int) -> int:
    return CODE_EXP[e_type](program=program,lines=lines,i=i,lines_len=lines_len)