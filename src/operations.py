from src import config
from src.exceptions import TypeMismatchException

def add_oper():
    if len(config.oper_stack) >= 2:
        op1 = config.oper_stack.pop()
        op2 = config.oper_stack.pop()

        if isinstance(op1, bool) or isinstance(op2, bool):
            # cannot add booleans in PS
            raise TypeMismatchException("Types of operands did not match")

        try:
            result = op1 + op2
        except:
            raise TypeMismatchException("Types of operands did not match")
        config.oper_stack.append(result)
    else:
        raise TypeMismatchException("Not enough operands for operation \"add\"")

def sub_oper():
    if len(config.oper_stack) >= 2:
        op1 = config.oper_stack.pop()
        op2 = config.oper_stack.pop()

        if isinstance(op1, bool) or isinstance(op2, bool):
            # cannot sub booleans in PS
            raise TypeMismatchException("Types of operands did not match")

        try:
            result = op2 - op1
        except:
            raise TypeMismatchException("Types of operands did not match")
        config.oper_stack.append(result)
    else:
        raise TypeMismatchException("Not enough operands for operation \"sub\"")
    
def mul_oper():
    if len(config.oper_stack) >= 2:
        op1 = config.oper_stack.pop()
        op2 = config.oper_stack.pop()

        if isinstance(op1, bool) or isinstance(op2, bool):
            # cannot mult booleans in PS
            raise TypeMismatchException("Types of operands did not match")

        try:
            result = op1 * op2
        except:
            raise TypeMismatchException("Types of operands did not match")
        config.oper_stack.append(result)
    else:
        raise TypeMismatchException("Not enough operands for operation \"mul\"")
    
def pop_oper():
    if len(config.oper_stack) >= 1:
        print(config.oper_stack.pop())
    else:
        raise TypeMismatchException("Not enough operands for operation \"=\"")