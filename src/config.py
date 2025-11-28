from src.ps_dict import PSDict
from src.operations import add_oper, sub_oper, mul_oper, pop_oper, def_oper, dict_oper, begin_oper, end_oper

# sets scoping
STATIC_SCOPING = False

# global stacks
oper_stack = []
dict_stack = []

def init_config():
    dict_stack.append(PSDict())

    dict_stack[-1]["add"] = add_oper
    dict_stack[-1]["sub"] = sub_oper
    dict_stack[-1]["mul"] = mul_oper
    dict_stack[-1]["="] = pop_oper
    dict_stack[-1]["def"] = def_oper
    dict_stack[-1]["dict"] = dict_oper
    dict_stack[-1]["begin"] = begin_oper
    dict_stack[-1]["end"] = end_oper