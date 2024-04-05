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
    def __init__(self,position,value=None,parameter_list=None,statement_list=None,return_statement=None):
        self._position = position
        self._value = value
        self._parameter_list = parameter_list or []
        self._statement_list = statement_list or []
        self._return_statement = return_statement
        
    def get_position():
        return self._position
    
    def set_value(self,value):
        self._value = value
        
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
        parameters = [p.get_value() for p in self._parameter_list]
        statements = ""
        for stmt in self._statement_list:
            statements += f"{stmt.get_statement_type()},{stmt.get_value()}:\n{stmt.get_statement()}\n" 
        if self._return_statement:
            statements += f"{self._return_statement.get_statement_type()},{self._return_statement.get_statement()}\n"
        return f"{self._value}{parameters}:\n" \
               f"{statements}"

class StatementType(Enum):
    ASSIGNMENT = auto()
    FUNCTION_CALL = auto()
    RETURN = auto()
    EXIT = auto()
    
class Statement():
    def __init__(self,position,statement_type=None,statement=None,value=None):
        self._position = position
        self._statement = statement
        self._type = statement_type
        self._value = value
        
    def get_position():
        return self._position
    
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
    def __init__(self,value:str,argument_list=None):
        self._value = value
        self._argument_list = argument_list or []
        
    def add_argument(self, argument):
        self._argument_list.append(argument)
        
    def get_value(self) -> str:
        return self._value
    
    def get_argument_list(self):
        return self._argument_list      
    
    def __repr__(self) -> str:
        return f"({self._value}:{[a for a in self._argument_list]})"
    
class Operator(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    
    def get_type(op:str)->(int,'Operator'):
        match(op):
            case '+':
                return True,Operator.ADD
            case '-':
                return True,Operator.SUB
            case '*':
                return True,Operator.MUL
            case '/':
                return True,Operator.DIV
            case _:
                return False,None
            
    def get_operator(self) -> str:
        match(self):
            case Operator.ADD:
                return '+'
            case Operator.SUB:
                return '-'
            case Operator.MUL:
                return '*'
            case Operator.DIV:
                return '/'
            case _:
                return None
               
class Expression():
    def __init__(self,expression_left=None,expression_right=None,operator:Operator=None,sub_exp=False):
        self._op = operator
        self._exp_left = expression_left
        self._exp_right = expression_right 
        self._sub_exp = sub_exp
        
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
    def is_sub_exp() -> bool:
        return self._sub_exp
    
    def get_data_types(self) -> []:
        data_types = []
        def _search_exp(left,right):
            if isinstance(left,Terminal):
                data_types.append((left.get_type(),left.get_value()))
            
            elif isinstance(left,Expression):
                _search_exp(left.get_expression_left(),left.get_expression_right())
                
            if isinstance(right,Terminal):
                data_types.append((right.get_type(),right.get_value()))
                print("possibru?")
                
            elif isinstance(right,Expression):
                _search_exp(right.get_expression_left(),right.get_expression_right())
                
        _search_exp(self.get_expression_left(),self.get_expression_right())
        return data_types
    
    def __repr__(self) -> str:        
        left = ""
        right = ""
        
        if self._exp_left.__class__ == self.__class__:
            for line in self._exp_left.__repr__().split('\n'):
                left += '-' + line + '\n'
        else:
            left = self._exp_left
            
        if self._exp_right.__class__ == self.__class__:
            for line in self._exp_right.__repr__().split('\n'):
                right += '-' + line + '\n'
        else:
            right = self._exp_right
            
        return f"{self.__class__.__name__}:\n{left}\n{self._op}\n{right}"

class TerminalType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    # LPAREN = auto()
    # RPAREN = auto()
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