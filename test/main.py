import sys,os
#import src
#from objects import*

def test_2():
    from mapper import map_it 
    return_code = None
    return_msg = None
    with open("test/examples/code1_fcob.txt","r") as file:
        text = file.read()
        return_code, return_msg = map_it(text)
    if return_code:
        print('End with success: ', return_msg)
    else:
        print('End with failure: ', return_msg)

def test_1():
    from objects import Variable,Section,Condition,Operation 
    v1 = Variable(ptype='int',scope='local')
    print(v1)
    op1 = Operation(opType='MOVE',variables=['SPACE',v1])
    print(op1) 

def main() -> int:
    try:
        import mapper,objects
        print("Module 'example_module' imported successfully!")
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