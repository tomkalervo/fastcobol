from objects import *
VARIABLE_DECLARE = [
    'u_int',
    'int',
    'string'
]
FUNCTION_SYSTEM = [
    'print'
]
FUNCTION_DECLARE = 'func'
FUNCTION_CALL = r'\b[a-zA-Z0-9]+\s*\('
VARIABLE_OPERATION = r'\b[a-zA-Z0-9]+\s*\='
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
    
    # Parse expression and add to program
    return_code,current_line = parse_expression(program,
                                                lines_of_code,
                                                current_line,
                                                total_lines)
    if return_code == ERROR:
        return ERROR
        
    current_line += 1
    # Recursive call
    return parse_program(program=program,
                         lines_of_code=lines_of_code,
                         current_line=current_line,
                         total_lines=total_lines) 

def evaluate_expression(e:str) -> (int,str,str):
    import re

    for v in VARIABLE_DECLARE:
        if e.strip().startswith(v):
            return OK,'vd',v
    
    match = re.match(VARIABLE_OPERATION, e)
    if match:
        return OK,'vo',match.group()
    
    for f in FUNCTION_SYSTEM:
        if e.strip().startswith(f):
            return OK,'fs',f
        
    if e.strip().startswith(FUNCTION_DECLARE):
        return OK,'fd',f
    
    match = re.match(FUNCTION_CALL, e)
    if match:
        return OK,'fc',match.group()

    return ERROR,'Incorrent line',e

def parse_VARIABLE_DECLARE(program:Program,
                           expression:list,
                           lines:list,
                           i:int,
                           lines_len:int) -> (int,int):
    print(f'parse_VARIABLE_DECLARE, {lines[i]}')
    if not expression:
        return ERROR,i
    else:
        ptype = expression.pop()
        
    if not expression:
        return ERROR,i
    else:
        name = expression[-1]

    if name not in program.data:
        v = Variable(ptype=ptype,name=name)
        if v.picType == None:
            return ERROR,i
        else:
            program.data[name] = v
        
    return parse_VARIABLE_OPERATION(program,expression,lines,i,lines_len)
def parse_VARIABLE_OPERATION(program:Program,
                           expression:list,
                           lines:list,
                           i:int,
                           lines_len:int) -> (int,int):
    print(f"parse_VARIABLE_OPERATION, {expression=}")
    if not expression:
        return ERROR,i
    
    x = expression.pop()
    if x not in program.data:
        return ERROR,i
    else:
        x_var = program.data[x]
    
    if not expression:
        return ERROR,i
    
    op = expression.pop()
    
    if op == ';':
        return OK,i
    
    if op != '=':
        return ERROR,i
    else:
        operation = Operation(variables=[x],opType=op)
    
    if not expression:
        return ERROR,i
    
    def is_type(s, type_conversion):
        try:
            type_conversion(s)
            return True
        except ValueError:
            return False

    while expression:
        y = expression.pop()
        print(f'{y=}')
        if y == ';':
            program.add_operation(operation)
            return OK,i
        if y[-1] == ';':
            y = y[:-1]
            expression.append(';')
        y_picType = None
        if y in program.data:
            y_var = program.data[y]
            y_picType = y_var.picType
        elif is_type(y,int):
            y_var = int(y)
            if y_var < 0:
                y_picType = ('int',len(y))
            else:
                y_picType = ('u_int',len(y))
        elif is_type(y,float):
            y_var = float(y)
            if y_var < 0:
                y_picType = ('float',len(y))
            else:
                y_picType = ('u_float',len(y))
        elif y[0] == y[-1] and y[0] in ['"',"'"] and len(y > 2):
            y_var = y[1:-1]
            y_picType = ('string',len(y_var))         
        #TODO elif an operation '+,-,*,/'
        # Every second item must be an operation...
        else:
            return ERROR, i       
        
        x_var.picType_operations.add(y_picType)        
        operation.variables.append(y_var)
    
    return ERROR,i

def parse_FUNCTION_SYSTEM(program:Program,
                           expression:list,
                           lines:list,
                           i:int,
                           lines_len:int) -> (int,int):

    return OK,i
def parse_FUNCTION_DECLARE(program:Program,
                           expression:list,
                           lines:list,
                           i:int,
                           lines_len:int) -> (int,int):
    print(f'get_function, {lines[i]}')
    return OK,i
def parse_FUNCTION_CALL(program:Program,
                           expression:list,
                           lines:list,
                           i:int,
                           lines_len:int) -> (int,int):
    print(f'user_get_function, {lines[i]}')
    return OK,i

CODE_EXP = {
    'vd':parse_VARIABLE_DECLARE,
    'vo':parse_VARIABLE_OPERATION,
    'fs':parse_FUNCTION_SYSTEM,
    'fd':parse_FUNCTION_DECLARE,
    'fc':parse_FUNCTION_CALL
}

def parse_expression(program:Program,lines:list,i:int,lines_len:int) -> (int,int):
    # Evaluate expression to prepare for builder
    line = lines[i]
    return_code,e_type,value = evaluate_expression(line)
    if return_code == ERROR:
        print(f'Error in evaluate_expression(): {e_type}. Expression value {value}')
        return (ERROR,i)
    expression = line.strip().split() # parse functions will pop one word/item at a time from the expression
    expression.reverse() # reverse because effecient to pop from tail (instead of head)
    print(f'{expression=}')
    return CODE_EXP[e_type](program=program,
                            expression=expression,
                            lines=lines,
                            i=i,
                            lines_len=lines_len)