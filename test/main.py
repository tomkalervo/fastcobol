import sys,os
# from my_token import tokenize
#from objects import*

def test_2():
    print("no test 2")

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
        import fc_token,fc_parse
        print(f"Module {fc_token} imported successfully!")
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