from src import config
from src.exceptions import TypeMismatchException, ZeroDivisionException, IndexOutOfRangeException
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

def length_oper():
    if len(config.oper_stack) < 1:
        raise TypeMismatchException("Not enough operands for operation \"length\"")

    op = config.oper_stack.pop()

    if isinstance(op, str):
        result = len(op)
    elif isinstance(op, PSDict):
        result = len(op.dict)  # use internal dict for key-count
    else:
        raise TypeMismatchException("Operand to \"length\" must be a string or dictionary")

    config.oper_stack.append(result)

def get_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operation \"get\"")

    index = config.oper_stack.pop()
    s = config.oper_stack.pop()

    if not isinstance(s, str):
        raise TypeMismatchException("Operand to \"get\" must be a string")
    if not isinstance(index, int):
        raise TypeMismatchException("String index must be an integer")
    if index < 0 or index >= len(s):
        raise IndexOutOfRangeException("String index out of range")

    config.oper_stack.append(ord(s[index]))

def getinterval_oper():
    if len(config.oper_stack) < 3:
        raise TypeMismatchException("Not enough operands for operation \"getinterval\"")

    count = config.oper_stack.pop()
    index = config.oper_stack.pop()
    s = config.oper_stack.pop()

    if not isinstance(s, str):
        raise TypeMismatchException("First operand must be a string")
    if not isinstance(index, int) or not isinstance(count, int):
        raise TypeMismatchException("Index and count must be integers")
    if index < 0 or count < 0 or index + count > len(s):
        raise IndexOutOfRangeException("Index/count out of range")

    substring = s[index:index + count]
    config.oper_stack.append(substring)

def putinterval_oper():
    if len(config.oper_stack) < 3:
        raise TypeMismatchException("Not enough operands for operation \"putinterval\"")

    source = config.oper_stack.pop()
    index = config.oper_stack.pop()
    target = config.oper_stack.pop()

    if not isinstance(source, str) or not isinstance(target, str):
        raise TypeMismatchException("Source and target must be strings")
    if not isinstance(index, int):
        raise TypeMismatchException("Index must be an integer")
    if index < 0 or index + len(source) > len(target):
        raise IndexOutOfRangeException("Index + length of source out of range")

    # Convert target to list to mutate
    target_list = list(target)
    for i, c in enumerate(source):
        target_list[index + i] = c

    new_target = "".join(target_list)
    config.oper_stack.append(new_target)
    
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

def eq_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operation \"eq\"")

    op1 = config.oper_stack.pop()
    op2 = config.oper_stack.pop()

    config.oper_stack.append(op1 == op2)

def ne_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operation \"ne\"")

    op1 = config.oper_stack.pop()
    op2 = config.oper_stack.pop()

    config.oper_stack.append(op1 != op2)

def ge_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operation \"ge\"")

    op1 = config.oper_stack.pop()
    op2 = config.oper_stack.pop()

    if not isinstance(op2, (int, float)) or not isinstance(op1, (int, float)):
        raise TypeMismatchException("Operands must be numbers")

    config.oper_stack.append(op2 >= op1)

def gt_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operation \"gt\"")

    op1 = config.oper_stack.pop()
    op2 = config.oper_stack.pop()

    if not isinstance(op2, (int, float)) or not isinstance(op1, (int, float)):
        raise TypeMismatchException("Operands must be numbers")

    config.oper_stack.append(op2 > op1)

def le_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operation \"le\"")

    op1 = config.oper_stack.pop()
    op2 = config.oper_stack.pop()

    if not isinstance(op2, (int, float)) or not isinstance(op1, (int, float)):
        raise TypeMismatchException("Operands must be numbers")

    config.oper_stack.append(op2 <= op1)

def lt_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operation \"lt\"")

    op1 = config.oper_stack.pop()
    op2 = config.oper_stack.pop()

    if not isinstance(op2, (int, float)) or not isinstance(op1, (int, float)):
        raise TypeMismatchException("Operands must be numbers")

    config.oper_stack.append(op2 < op1)

def and_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operation \"and\"") 

    op1 = config.oper_stack.pop()
    op2 = config.oper_stack.pop()

    # boolean and
    if isinstance(op2, bool) and isinstance(op1, bool):
        config.oper_stack.append(op2 and op1)
        return

    # integer bitwise and
    if type(op2) is int and type(op1) is int:
        config.oper_stack.append(op2 & op1)
        return

    # type mismatch
    raise TypeMismatchException("Operands to \"and\" must both be booleans or both integers")

def not_oper():
    if len(config.oper_stack) < 1:
        raise TypeMismatchException("Not enough operands for operator \"not\"")

    op = config.oper_stack.pop()

    # bool logical not
    if type(op) is bool:
        config.oper_stack.append(not op)
        return

    # int bitwise not
    if type(op) is int:
        config.oper_stack.append(~op)
        return

    raise TypeMismatchException("Operand to \"not\" must be boolean or integer")

def or_oper():
    if len(config.oper_stack) < 2:
        raise TypeMismatchException("Not enough operands for operator \"or\"")

    op1 = config.oper_stack.pop()
    op2 = config.oper_stack.pop()

    # Boolean OR
    if type(op2) is bool and type(op1) is bool:
        config.oper_stack.append(op2 or op1)
        return

    # Integer bitwise OR (bools excluded!)
    if type(op2) is int and type(op1) is int:
        config.oper_stack.append(op2 | op1)
        return

    raise TypeMismatchException("Operands to \"or\" must both be booleans or both be integers")