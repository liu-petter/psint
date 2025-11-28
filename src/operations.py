from src import config
from src.exceptions import TypeMismatchException
from src.ps_dict import PSDict

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
    
def def_oper():
    if len(config.oper_stack) >= 2:
        value = config.oper_stack.pop()
        key = config.oper_stack.pop()
        if isinstance(key, str) and key.startswith("/"):
            key = key[1:]
            config.dict_stack[-1][key] = value
        else:
            config.oper_stack.append(key)
            config.oper_stack.append(value)
            raise TypeMismatchException(f"Unable to define {key} with {value}")
    else:
        raise TypeMismatchException("Not enough operands for operation \"mul\"")
    
def dict_oper():
    new_dict = PSDict()
    if config.STATIC_SCOPING:
        current_dict = config.dict_stack[-1]
        new_dict.set_parent(current_dict)
    config.oper_stack.append(new_dict)

def begin_oper():
    if len(config.oper_stack) >= 1:
        dict_obj = config.oper_stack.pop()
        if isinstance(dict_obj, PSDict):
            config.dict_stack.append(dict_obj)
        else:
            raise TypeMismatchException("Top of operand stack is not a dictionary")
    else:
        raise TypeMismatchException("Stack is empty")
    
def end_oper():
    if len(config.dict_stack) > 1:
        config.dict_stack.pop()
    else:
        raise TypeMismatchException("Cannot end default dictionary")