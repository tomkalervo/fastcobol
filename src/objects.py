class Variable:
    picType = None       
    name = None
    scope = None  
    def __init__(self,picType='X',name='AA-NAME',scope='global') -> None:  
        self.picType = picType       
        self.name = name
        self.scope = scope     
    def __str__(self) -> str:
        return f"Variable instance: <{self.name} PIC {self.picType}> declared at a {self.scope} scope."

class Section:
    name = None
    conditions = []
    operations = []
    
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
    name = None
    data = None
    code = None
    def __init__(self,name='unnamed') -> None:    
        self.name = name 
        self.data = []
        self.code = []
    def __str__(self) -> str:
        return f"Program instance: <name={self.name}, lines of data={len(self.data)}, lines of code={len(self.code)}>"
    
class Comment:
    text = None
    def __init__(self,text: str) -> None:    
        self.text = text 