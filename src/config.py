from src.ps_dict import PSDict
from src.operations import add_oper, sub_oper, mul_oper, pop_oper, def_oper

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