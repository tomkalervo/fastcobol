from fc_ast import *

SETTINGS = {
    'indicator_area' : 8,
    'area_a' : 13,
    'comment_area' : 74,
    'condition_spacing' : 2,
    'data_group_increment' : 5,
    'data_switch_level' : 88
}

class DataDivision:
    def __init__(self) -> None:
        self._storage = {}
        
    def add_with_expression(self,var:str,exp:Expression) -> None:
        data_types = exp.get_data_types()
        print(f"Data Types in {var}: {data_types}")
        if var in self._storage:
            self._storage[var].append(data_types)
        else:
            self._storage[var] = data_types 

    def get_storage(self) -> dict:
        return self._storage

def build(program:Program,settings:dict) -> (int,str):
    #TODO incorporate custom settings
    cobol = "IDENTIFICATION DIVISION.\n"
    name = program.get_value()
    if not name:
        return False,"No valid program-name"
    else:
        cobol += f"PROGRAM-ID. {cobolize_var_name(name)}.\n"
        
    data = DataDivision()
    proc_div = []
    for stmt in program.get_statement_list():
        retcode,msg = _build_statements(proc_div,stmt,data)
        if retcode == False:
            return retcode,msg
        
    print(f"{data._storage=}")
    cobol += "DATA DIVISION.\n"
    cobol += SETTINGS['indicator_area'] * ' ' + "WORKING-STORAGE SECTION.\n"
    store = data.get_storage()
    for var in store:
        print(f"{store[var][0]=}")
        _type,val = store[var][0]
        row = SETTINGS['area_a'] * ' '
        level = 1
        match(_type):
            case TerminalType.INTEGER:
                digit_size = "09"
                row += f"{level} {var} PIC S9({digit_size})     BINARY.\n"
            case TerminalType.IDENTIFIER:
                row += f"{level} {var} PIC  Z(08)9(1).\n"
                
        cobol += row
        
    cobol += "PROCEDURE DIVISION.\n"
    for line in proc_div:
        row = SETTINGS['indicator_area'] * ' ' + line
        if len(row) <= 80:
            cobol += row + '.\n'
        else:
            print(f"Row length > 80, {row=}")
            
    cobol += "STOP RUN.\n"
    
    return True,cobol

def _build_statements(proc_div:list,stmt:Statement,data:DataDivision) -> (int,str):
    match(stmt.get_statement_type()):
        case StatementType.ASSIGNMENT:
            data.add_with_expression(var=stmt.get_value(),exp=stmt.get_statement())
            code = _build_assignment(var=stmt.get_value(),exp=stmt.get_statement())
            proc_div.append(code)
        case StatementType.FUNCTION_CALL:
            pass 
        case _: 
            return False,f"Invalid Statement Type {stmt.get_statement_type()} in statement {stmt.get_value()}"
        
    return True,'ok'

def _build_assignment(var:str,exp:Expression) -> str:
    code = ""
    if exp.get_operator():
        # Compute, Add, Sub etc
        code = f"COMPUTE {cobolize_var_name(var)} = "
        def build_exp(left,right,op):
            nonlocal code

            if isinstance(left,Terminal):
                code += left.get_value()
            elif isinstance(left,Expression):
                code += '('
                build_exp(left.get_expression_left(),left.get_expression_right(),left.get_operator())
                code += ')'
                
            if isinstance(op,Operator):
                code += ' ' + op.get_operator() + ' '
                
            if isinstance(right,Terminal):
                code += right.get_value()
            elif isinstance(right,Expression):
                build_exp(right.get_expression_left(),right.get_expression_right(),right.get_operator())
                
        build_exp(exp.get_expression_left(),exp.get_expression_right(),exp.get_operator())

    else:
        code = f"MOVE {exp.get_expression_left().get_value()} TO {cobolize_var_name(var)}"
    
    return code

def cobolize_var_name(name:str) -> str:
    return name.upper().replace('_', '-')