# SETTINGS
MAIN_EXIT = 'GOBACK'
WORKING_STORAGE_LEVELS = (1,5), 5

class Variable:
    picType = None       
    name = None
    scope = None  
    display = None
    def __init__(self,picType='X',name='AA-NAME',scope='global',display=False) -> None:  
        self.picType = picType       
        self.name = name
        self.scope = scope     
        self.display = display
    def __str__(self) -> str:
        return f"Variable instance: <{self.name} PIC {self.picType}> declared at a {self.scope} scope."
    
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
    
class Section:
    name = None
    exit_routine = None
    conditions = []
    operations = []
    def __init__(self,name:str,variables=[],operations=[],exit_routine=Operation(opType='CONTINUE')) -> None:  
        self.name = name       
        self.variables = variables
        self.operations = operations
        self.exit_routine = exit_routine

    def __str__(self) -> str:
        return f"Section instance: <{self.name} "\
                "with exit routine {self.exit_routine}, "\
                "conditions={len(self.conditions)}, "\
                "operations={len(self.operations)}>"
    
    
class Program:
    name = None
    data = None
    procedure = None
    section = None
    def __init__(self,name='unnamed') -> None:    
        self.name = name 
        self.data = {}
        main = Section(name='main',exit_routine=Operation(opType=MAIN_EXIT))
        self.section = {'main':main}
        self.procedure = []
        
    def __str__(self) -> str:
        return f"Program instance: <name={self.name}, "\
                "lines of data={len(self.data)}, "\
                "elements in procedure={len(self.procedure)}>"
                
    def add_procedure(self,proc,variables:list) -> None:
        """_summary_

        Args:
            proc (Operation, Comment): Procedure to add to the program
            variables (list): list of variables used in the procedure
        """
        self.procedure.append(proc)
        for v in variables:
            if v.name in self.data:
                self.data[v.name]['reference'].append(proc)
            else:
                self.data[v.name] = {'reference':[proc],'variable':v}
                
    def add_section(self,sec:Section,variables:list) -> int:
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
class Comment:
    text = None
    def __init__(self,text: str) -> None:    
        self.text = text 