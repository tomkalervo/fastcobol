class Node:
    def __init__(self,value,position,parent=None) -> None:
        self._position = position
        self._parent = parent
        self._value = value
        
    def set_value(self, value) -> None:
        self._value = value

    def set_parent(self, parent:'Node') -> None:
        self._parent = parent
        
    def get_parent(self) -> 'Node':
        return self._parent
    
    def get_value(self) -> str:
        return self._value
        
    def __repr__(self) -> str:
        return f"Node type={type(self)}({self._value=}, {self._parent=})"
   
class ProgramNode(Node):
    def __init__(self,value,position,function_list=[],statement_list=[]) -> None:
        super().__init__(value=value,position=position,parent=None)
        self.function_list = function_list
        self.statement_list = statement_list
        
    def get_function_list(self) -> list:
        return self.function_list
    
    def statement_list(self) -> list:
        return self.statement_list
    
    def __repr__(self) -> str:
        context = super().__repr__()
        return f"{context}, {self.function_list=}, {self.statement_list=}"
   
class FunctionNode(Node):
    def __init__(self,value,position,parent,parameter_list=[],statement_list=[],return_statement=None):
        super().__init__(value=value,position=position,parent=parent)
        self.parameter_list = parameter_list
        self.statement_list = statement_list
        self.return_statement = return_statement
        
    def get_parameter_list(self) -> list:
        return self.parameter_list
    
    def get_statement_list(self) -> list:
        return self.statement_list
    
    def get_return_statement(self) -> 'Node':
        self.return_statement
        
    def __repr__(self) -> str:
        context = super().__repr__()
        return f"{context}, {self.parameter_list=}, {self.statement_list=}, {self.return_statement=}"
    
class StatementNode(Node):
    def __init__(self,value,position,parent):
        super().__init__(value=value,position=position,parent=parent)
        
    def __repr__(self) -> str:
        context = super().__repr__()
        return f"{context}"