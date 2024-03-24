class Node:
    def __init__(self,position,value=None,parent=None) -> None:
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
        return f"Node type={type(self)}({self._value=})"
   
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
        self._parameter_list = parameter_list
        self._statement_list = statement_list
        self._return_statement = return_statement
        
    def add_parameter(self, parameter:'Node'):
        self._parameter_list.append(parameter)
        
    def add_statement(self, statement:'Node'):
        self._statement_list.append(statement)
        
    def add_return_statement(self, return_statement:'Node'):
        self._return_statement = return_statement
        
    def get_parameter_list(self) -> list:
        return self._parameter_list
    
    def get_statement_list(self) -> list:
        return self._statement_list
    
    def get_return_statement(self) -> 'Node':
        self._return_statement
        
    def __repr__(self) -> str:
        context = super().__repr__()
        return f"{context}, {self._parameter_list=}, {self._statement_list=}, {self._return_statement=}"
    
class StatementNode(Node):
    def __init__(self,value,position,parent,statement=None):
        super().__init__(value=value,position=position,parent=parent)
        self._child=statement
        
    def set_statement(self,statement):
        self._child=statement
        
    def get_statement(self):
        return self._child
    
    def __repr__(self) -> str:
        context = super().__repr__()
        return f"{context}"
    
class ReturnNode(Node):
    def __init__(self,value,position,parent,expression=None):
        super().__init__(value=value,position=position,parent=parent)
        self._expression=expression
        
    def __repr__(self) -> str:
        context = super().__repr__()
        return f"{context},{self._expression=}"
    
class IdentifierNode(Node):
    def __init__(self,value,position,parent):
        super().__init__(value=value,position=position,parent=parent)
        
class BinaryOperationNode(Node):
    def __init__(self,value,position,operator,left=None,right=None):
        super().__init__(value=value,position=position,parent=parent)
        self._operator = operator
        self._left = left
        self._right = right
        
class FunctionCallNode(Node):
    def __init__(self,position,parent,value,argument_list=None):
        super().__init__(value=value,
                         position=position,
                         parent=parent)
        self._argument_list = argument_list
        
    def add_argument(self, argument:'Node'):
        self._argument_list.append(argument)
        
    def get_argument_list(self):
        return self._argument_list      
    
class ExpressionNode(Node):
    def __init__(self,position,parent,value):
        super().__init__(value=value,
                         position=position,
                         parent=parent)
        self._operator = None
        self._expression_left = None 
        self._expression_right = None 
        
    def set_operator(self,op):
        self._operator = op
    def set_expression_left(self,exp):
        self._expression_left = exp 
    def set_expression_right(self,exp):
        self._expression_right = exp 
        
    def get_operator(self):
        return self._operator
    def get_expression_left(self):
        return self._expression_left
    def get_expression_right(self):
        return self._expression_right 
    
    def __repr__(self) -> str:
        context = super().__repr__()
        
        return f"{context},{self._expression_left=},{self._operator=},{self._expression_right=}"

class TermNode(Node):
    def __init__(self,value,position,parent,term=None):
        super().__init__(value=value,position=position,parent=parent)
        self._term=token
        
    def set_term(self,term):
        self._term=term
        
    def get_term(self):
        return self._term