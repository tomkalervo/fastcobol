import sys,os
#import src
#from objects import*

def test_1():
    from mapper import map_it 
    from objects import Variable,Section,Condition,Operation 
    v1 = Variable(picType='X(03)',scope='local')
    print(v1)
    op1 = Operation(opType='MOVE',variables=['SPACE',v1])
    print(op1)
    map_it()
    

def main() -> int:
    try:
        import mapper,objects
        print("Module 'example_module' imported successfully!")
    except ImportError:
        print("Failed to import 'example_module'")
    test_1()
    return 0
    
if __name__ == '__main__':
    path = os.getcwd() + '/src'
    sys.path.insert(0, path)
    sys.exit(main())