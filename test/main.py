import sys,os
# from my_token import tokenize
#from objects import*

def test_2():
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
        
        ass1 = Statement(statement=exp1,statement_type=StatementType.ASSIGNMENT,value=x)
        # print(ass1)
        
        p.add_statement(ass1)
        
        exp2 = Expression(expression_left=int_5,expression_right=int_3,operator=Operator.SUB)
        # print(exp1)
        
        ass2 = Statement(statement=exp2,statement_type=StatementType.ASSIGNMENT,value=x)
        # print(ass1)
        
        p.add_statement(ass2)

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
        from fc_parse import build_parse_tree
        print('___' * 30)
        parse_tree = build_parse_tree(tokens)
        print('AST COMPLETE')
        print(parse_tree)
    else:
        print('End with failure: ', return_msg)
    # for t in tokens:
    #     print(t)

def main() -> int:
    try:
        import fc_token,fc_parse,fc_ast
        print(f"Module {fc_token},{fc_parse},{fc_ast} imported successfully!")
    except ImportError:
        print("Failed to import 'example_module'")
    print('='*20,'test1','='*20)
    test_1()
    print('='*20,'test2','='*20)
    test_2()
    return 1
    
if __name__ == '__main__':
    path = os.getcwd() + '/src'
    sys.path.insert(0, path)
    sys.exit(main())