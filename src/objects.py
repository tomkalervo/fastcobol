# SETTINGS
MAIN_EXIT = 'GOBACK'
WORKING_STORAGE_LEVELS = (1,5), 5

class Variable:
    types = {
        'u_int':('9',12),
        'int':('S9',12),
        'string':('X',30)
    }
    def parseType(self,ptype:str) -> None:
        ptype_info = ptype.split('(')
        if len(ptype_info) > 1:
            p = ptype_info[0]
            [size] = ptype_info[1].strip(')')
            print(p,size)
            if p in types and size.isNumeric():
                self.picType = (p,int(size))
        else:
            if ptype in self.types:
                self.picType = self.types[ptype]
        
    def __init__(self,ptype:str,name='AA-NAME',scope='global',display=False) -> None:  
        self.parseType(ptype)
        self.name = name
        self.scope = scope     
        self.display = display
        self.picType_operations = set()
        
    def __str__(self) -> str:
        return f"Variable instance: <{self.name} PIC {self.picType}> declared at a {self.scope} scope."
    
    # def __add__(self,other:'Variable') -> None:
    #     self.picType_operations.add(other.picType)
    
class Operation:
    opType = None
    variables = []
    def __init__(self,opType='CONTINUE',variables=[]) -> None:  
        self.opType = opType       
        self.variables = variables

    def __str__(self) -> str:
        list_v = [x.name if type(x) == Variable else x for x in self.variables]
        return f"Operation instance: <{self.opType} on variables: {list_v}>"
    
class Condition:
    conType = None
    conTrue = []    # List of tuples (condition,list of operations)
                    # or List of operations to run on true
    conFalse = []   # List of operations to run on false
        
class Program:
    def __init__(self,name='unnamed') -> None:    
        self.name = name 
        self.data = {}
        self.section = {}
        self.procedure = []
        
    def __str__(self) -> str:
        return f"Program instance: <name={self.name}, "\
               f"data items={len(self.data)}, "\
               f"elements in procedure={len(self.procedure)}>"
                
    def add_operation(self,operation:Operation) -> None:
        self.procedure.append(operation)
                
    def add_section(self,sec,variables:list) -> int:
        """_summary_

        Args:
            sec (Section): _description_
            variables (list): _description_

        Returns:
            int: True if ok, else False
        """
        if sec.name in self.section:
            return 0, f"Dublicate occurences of Section [{self.section[sec.name]},{sec}]"
        self.section[sec.name] = sec
        for v in variables:
            if v.name in self.data:
                self.data[v.name]['reference'].append(proc)
            else:
                self.data[v.name] = {'reference':[proc],'variable':v}
        return 1, "ok"
    
class Section(Program):
    exit_routine = None
    def __init__(self,name:str,exit_routine=Operation(opType='CONTINUE')) -> None:  
        super().__init__(name)
        self.exit_routine = exit_routine

    def __str__(self) -> str:
        return f"Section instance: <{self.name} "\
               f"with exit routine {self.exit_routine}, "\
               f"conditions={len(self.conditions)}, "\
               f"operations={len(self.operations)}>"
               
class Comment:
    text = None
    def __init__(self,text: str) -> None:    
        self.text = text 