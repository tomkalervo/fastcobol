import os
import sys

# Add the 'src' directory to the Python module search path
path = os.getcwd() + '/src'
sys.path.insert(0, path)

# Import local modules
import fc_token
import fc_parse
import fc_ast

def test_ast_functions():
    from fc_ast import Program,Statement,StatementType,Expression,Terminal,TerminalType,Operator

    def get_structure() -> Program:
        p = Program(value="MY-PROG")
        
        # x = 5 + 3
        x = Terminal(position=1,value="x",terminal_type=TerminalType.IDENTIFIER)
        int_5 = Terminal(position=1,value="5",terminal_type=TerminalType.INTEGER)
        int_3 = Terminal(position=1,value="3",terminal_type=TerminalType.INTEGER)
        # print(f"{x=}\n{int_5=}\n{int_3=}")
        
        exp1 = Expression(expression_left=int_5,expression_right=int_3,operator=Operator.ADD)
        # print(exp1)
        
        ass1 = Statement(position=1,statement=exp1,statement_type=StatementType.ASSIGNMENT,value=x)
        # print(ass1)
        
        p.add_statement(ass1)
        
        # y = x * 1.2
        y = Terminal(position=2,value="y",terminal_type=TerminalType.IDENTIFIER)
        float_1_2 = Terminal(position=2,value="1.2",terminal_type=TerminalType.FLOAT)

        exp2 = Expression(expression_left=x,expression_right=float_1_2,operator=Operator.MUL)
        print(exp2)
        
        ass2 = Statement(position=2,statement=exp2,statement_type=StatementType.ASSIGNMENT,value=y)
        print(ass2)
        
        p.add_statement(ass2)

        # z = y / (x - 2)
        z = Terminal(position=3,value="z",terminal_type=TerminalType.IDENTIFIER)
        int_2 = Terminal(position=3,value="2",terminal_type=TerminalType.INTEGER)
        exp3 = Expression(expression_left=x,expression_right=int_2,operator=Operator.SUB)
        exp4 = Expression(expression_left=y,expression_right=exp3,operator=Operator.DIV)
        ass3 = Statement(position=3,statement=exp4,statement_type=StatementType.ASSIGNMENT,value=z)
        p.add_statement(ass3)
        
        return p
    
    prog = get_structure()
    print(prog)
    print("done")

def test_1():
    return_code = None
    return_msg = None
    with open("test/examples/code2_fcob.txt","r") as file:
        text = file.read()
        # Tokenize the program string
        from fc_token import tokenize
        return_code,return_msg,tokens = tokenize(text)
    if return_code:
        print('End with success: ', return_msg)
        # Build the parse tree or AST from the tokens
        from fc_parse import parse
        print('___' * 30)
        return_code,message,ast_prog = parse(tokens)
        print('AST COMPLETE')
        if return_code:
            print("Parse success:")
            assert(ast_prog.get_function_list()[1].get_statement_list() != ast_prog.get_function_list()[0].get_statement_list())

            print(f"{ast_prog=}")
            return ast_prog
        else:
            print(f'Parse fail: {message}')
    else:
        print('End with failure: ', return_msg)

    return None
def test_2(prog:'Program'):
    print("Start test...")
    return True
def main() -> int:
    print('='*20,'test1','='*20)
    ast_prog = test_1()
    print('='*20,'test2','='*20)
    test_2(ast_prog)
    return 1
    
if __name__ == '__main__':
    sys.exit(main())