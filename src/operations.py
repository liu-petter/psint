from src import config
from src.exceptions import TypeMismatchException, ZeroDivisionException
from src.ps_dict import PSDict
import math

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
    
def idiv_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operation \"idiv\"")

    op1 = config.oper_stack.pop()
    op2 = config.oper_stack.pop()

    if not isinstance(op2, (int, float)) or not isinstance(op1, (int, float)):
        raise TypeMismatchException("Operands to 'idiv' must be numeric")

    if op1 == 0:
        raise ZeroDivisionException("Division by zero in \"idiv\"")

    result = int(op2 / op1)

    config.oper_stack.append(result)

    
def div_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operation \"div\"")

    op1 = config.oper_stack.pop()
    op2 = config.oper_stack.pop()

    if not (isinstance(op1, (int, float)) and isinstance(op2, (int, float))):
        raise TypeMismatchException("Operands to \"div\" must be numbers")

    if op1 == 0:
        raise ZeroDivisionException("Division by zero in \"div\"")

    result = float(op2) / float(op1)

    config.oper_stack.append(result)

def mod_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operation \"mod\"")

    op1 = config.oper_stack.pop()
    op2 = config.oper_stack.pop()

    if not isinstance(op1, int) or not isinstance(op2, int):
        raise TypeMismatchException("Operands to \"mod\" must be integers")

    if op1 == 0:
        raise ZeroDivisionException("Division by zero in \"mod\"")

    result = op2 - op1 * int(op2 / op1)

    config.oper_stack.append(result)

def abs_oper():
    if len(config.oper_stack) < 1:
        raise TypeMismatchException("Not enough operands for operation \"abs\"")

    op = config.oper_stack.pop()

    if not isinstance(op, (int, float)):
        raise TypeMismatchException("Operand to \"abs\" must be a number")

    result = abs(op)

    config.oper_stack.append(result)

def neg_oper():
    if len(config.oper_stack) < 1:
        raise TypeMismatchException("Not enough operands for operation \"neg\"")

    op = config.oper_stack.pop()

    if not isinstance(op, (int, float)):
        raise TypeMismatchException("Operand to \"neg\" must be numeric")

    result = -op

    config.oper_stack.append(result)

def ceiling_oper():
    if len(config.oper_stack) < 1:
        raise TypeMismatchException("Not enough operands for operation \"ceiling\"")

    op = config.oper_stack.pop()

    if not isinstance(op, (int, float)):
        raise TypeMismatchException("Operand to \"ceiling\" must be a number")

    result = int(math.ceil(op))

    config.oper_stack.append(result)

def floor_oper():
    if len(config.oper_stack) < 1:
        raise TypeMismatchException("Not enough operands for operation \"floor\"")

    op = config.oper_stack.pop()

    if not isinstance(op, (int, float)):
        raise TypeMismatchException("Operand to \"floor\" must be a number")

    result = int(math.floor(op))

    config.oper_stack.append(result)

def round_oper():
    if len(config.oper_stack) < 1:
        raise TypeMismatchException("Not enough operands for operator \"round\"")

    op = config.oper_stack.pop()

    if not isinstance(op, (int, float)):
        raise TypeMismatchException("Operand to \"round\" must be a number")

    if op > 0:
        result = int(op + 0.5)
    else:
        result = int(op - 0.5)

    config.oper_stack.append(result)
    
def sqrt_oper():
    if len(config.oper_stack) < 1:
        raise TypeMismatchException("Not enough operands for operations \"sqrt\"")

    op = config.oper_stack.pop()

    if not isinstance(op, (int, float)):
        raise TypeMismatchException("Operand to \"sqrt\" must be a number")

    if op < 0:
        raise TypeMismatchException("Cannot compute square root of negative number")

    result = math.sqrt(op)
    config.oper_stack.append(result)

def equal_oper():
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
    
def exch_oper():
    if len(config.oper_stack) >= 2:
        op1 = config.oper_stack.pop()
        op2 = config.oper_stack.pop()
        config.oper_stack.append(op1)
        config.oper_stack.append(op2)
    else:
        raise TypeMismatchException("Not enough operands for operation \"exch\"")

def pop_oper():
    if len(config.oper_stack) >= 1:
        config.oper_stack.pop()
    else:
        raise TypeMismatchException("Not enough operands for operation \"=\"")

def copy_oper():
    if not config.oper_stack:
        raise TypeMismatchException("Operand stack is empty for 'copy'")

    top = config.oper_stack.pop()

    # Copy top N elements if top is int
    if isinstance(top, int):
        n = top
        if n < 0 or n > len(config.oper_stack):
            raise TypeMismatchException("Not enough elements to copy")
        slice_to_copy = config.oper_stack[-n:]
        config.oper_stack.extend(slice_to_copy)

    # Copy array or string
    elif isinstance(top, list):
        config.oper_stack.append(top.copy())  # shallow copy
    elif isinstance(top, str):
        config.oper_stack.append(str(top))    # new string
    else:
        raise TypeMismatchException(f"Cannot copy object of type {type(top)}")
    
def dup_oper():
    if len(config.oper_stack) >= 1:
        op = config.oper_stack[-1]
        config.oper_stack.append(op)
    else:
        raise TypeMismatchException("Not enough operands for operation \"dup\"")

def clear_oper():
    config.oper_stack.clear()

def count_oper():
    config.oper_stack.append(len(config.oper_stack))
