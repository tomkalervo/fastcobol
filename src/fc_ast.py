from enum import Enum, auto
   
class Program():
    def __init__(self,value,function_list=[],statement_list=[]) -> None:
        self._value=value
        self.function_list = function_list
        self.statement_list = statement_list
        
    def get_value(self) -> str:
        return self._value

    def get_function_list(self) -> list:
        return self.function_list
    
    def get_statement_list(self) -> list:
        return self.statement_list
    
    def add_statement(self,statement) -> None:
        self.statement_list.append(statement)
    
    def add_function(self,function) -> None:
        self.function_list.append(function)
    
    def __repr__(self) -> str:
        n_statements = len(self.statement_list)
        statements_str = ""
        for i,s in enumerate(self.statement_list):
            statements_str += f"({i+1}/{n_statements}): {s}\n"
        
        return f"{self.__class__.__name__}:{self._value}\n" \
               f">Statements:\n{statements_str}" \
               f">Functions:\n{[f for f in self.function_list]}"
   
class Function():
    def __init__(self,value=None,parameter_list=[],statement_list=[],return_statement=None):
        self._value = value
        self._parameter_list = parameter_list
        self._statement_list = statement_list
        self._return_statement = return_statement
        
    def set_value(self,value):
        self._value=value
        
    def get_value(self):
        return self._value
         
    def add_parameter(self,parameter):
        self._parameter_list.append(parameter)
        
    def add_statement(self,statement):
        self._statement_list.append(statement)
        
    def add_return_statement(self,return_statement):
        self._return_statement = return_statement
        
    def get_parameter_list(self) -> list:
        return self._parameter_list
    
    def get_statement_list(self) -> list:
        return self._statement_list
    
    def get_return_statement(self):
        self._return_statement
        
    def __repr__(self) -> str:
        return f"{self._value}, {self._parameter_list=}, {self._statement_list=}, {self._return_statement=}"

class StatementType(Enum):
    ASSIGNMENT = auto()
    FUNCTION_CALL = auto()
    RETURN = auto()
    EXIT = auto()
    
class Statement():
    def __init__(self,statement_type=None,statement=None,value=None):
        self._statement=statement
        self._type=statement_type
        self._value = value
        
    def set_statement(self,statement):
        self._statement=statement

    def set_identifier(self,value):
        self._value=value
        
    def get_statement(self):
        return self._statement
        
    def get_identifier(self):
        return self._value
    
    def set_statement_type(self,_type):
        self._type=_type
        
    def get_statement_type(self):
        return self._type
    
    def set_value(self,value:'Terminal'):
        self._value=value
    
    def get_value(self):
        return self._value
    
    def __repr__(self) -> str:
        if self.get_statement_type() == StatementType.ASSIGNMENT:
            string_rep = f"{self._type}\n{'-'}{self._value} :="
            for line in self._statement.__repr__().split():
                string_rep += f"\n{'-'*2}{line}"
            return string_rep + '\n'
        else:
            return f"{self._type}(\n{self._statement}\n)"
        
class FunctionCall():
    def __init__(self,value:str,argument_list=[]):
        self._value = value
        self._argument_list = argument_list
        
    def add_argument(self, argument):
        self._argument_list.append(argument)
        
    def get_argument_list(self):
        return self._argument_list      

class Operator(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    
class Expression():
    def __init__(self,expression_left=None,expression_right=None,operator:Operator=None):
        self._op = operator
        self._exp_left = expression_left
        self._exp_right = expression_right 
        
    def set_operator(self,operator:Operator):
        self._op = operator
    def set_expression_left(self,expression):
        self._exp_left = expression 
    def set_expression_right(self,expression):
        self._exp_right = expression 
        
    def get_operator(self):
        return self._op
    def get_expression_left(self):
        return self._exp_left
    def get_expression_right(self):
        return self._exp_right 
    
    def __repr__(self) -> str:        
        left = ""
        for e in self._exp_left.__repr__().split():
            left += '-' + e + '\n'
        right = ""
        for e in self._exp_right.__repr__().split():
            right += '-' + e + '\n'
        return f"{self.__class__.__name__}:\n{left}\n-{self._op}\n{right}\n"

class TerminalType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    LPAREN = auto()
    RPAREN = auto()
    IDENTIFIER = auto()
    
class Terminal():
    def __init__(self,value:str,position,terminal_type:TerminalType):
        self._value=value
        self._position=position
        self._type=terminal_type
        
    def set_type(self,terminal_type):
        self._type=terminal_type
        
    def get_type(self):
        return self._type
            
    def set_value(self, value) -> None:
        self._value = value
    
    def get_value(self) -> str:
        return self._value
    
    def get_position(self):
        return self._position
        
    def __repr__(self) -> str:
        return f"Terminal({self._type},{self._value},{self._position})"