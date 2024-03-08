from objects import *

def map_it(text: str) -> (int,str):
    if not text:
        return 0, 'Empty text'
    rows = []
    row_i = 0
    lines = text.splitlines()
    lines_len = len(lines)
    # Check that Program is declared and enclosed
    while(lines[row_i].startswith('Program') != True):
        if len(lines[row_i]) == 0:
            continue
        elif lines[row_i] == '*':
            rows.append(Comment(lines[row_i]))
        else:
            return 0, 'Incorrect Program declaration'
        
        row_i += 1
        if row_i >= lines_len:
            return 0, 'Missing Program start-statement'

    program_statement = lines[row_i].split()
    if(len(program_statement) != 3 or program_statement[2] != '{'):
        return 0, "Incorrect Program declaration statement"
    
    prog = Program(name=program_statement[1])
    row_i += 1
    while(len(lines[row_i]) != 1 and lines[row_i][0] != '}'):
        prog.code.append(lines[row_i])
        
        row_i += 1
        if row_i >= lines_len:
            return 0, 'Missing Program end-statement'
    
    
    print("Map it complete!")
    print(prog)
    for i,code in enumerate(prog.code):
        print(f"{i}:\t{code}")
        
    return 1, 'ok'
