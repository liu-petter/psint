from src.ps_dict import PSDict
import src.operations as ops

# sets scoping
STATIC_SCOPING = False

# global stacks
oper_stack = []
dict_stack = []

# used to differentiate functions that require executing code blocks
# check func if in list to pass input_parser into func so no import loops
exec_funcs = ["if", "ifelse", "for", "repeat"]

def init_config():
    # default dictionary
    dict_stack.append(PSDict())

    # math operations
    dict_stack[-1]["add"] = ops.add_oper
    dict_stack[-1]["sub"] = ops.sub_oper
    dict_stack[-1]["mul"] = ops.mul_oper
    dict_stack[-1]["div"] = ops.div_oper
    dict_stack[-1]["idiv"] = ops.idiv_oper
    dict_stack[-1]["mod"] = ops.mod_oper
    dict_stack[-1]["abs"] = ops.abs_oper
    dict_stack[-1]["neg"] = ops.neg_oper
    dict_stack[-1]["ceiling"] = ops.ceiling_oper
    dict_stack[-1]["floor"] = ops.floor_oper
    dict_stack[-1]["round"] = ops.round_oper
    dict_stack[-1]["sqrt"] = ops.sqrt_oper

    # output operations
    dict_stack[-1]["="] = ops.equal_oper
    dict_stack[-1]["print"] = ops.print_oper
    dict_stack[-1]["=="] = ops.eqeq_oper

    # dictionary operations
    dict_stack[-1]["def"] = ops.def_oper
    dict_stack[-1]["dict"] = ops.dict_oper
    dict_stack[-1]["begin"] = ops.begin_oper
    dict_stack[-1]["end"] = ops.end_oper
    dict_stack[-1]["length"] = ops.length_oper

    # string operations
    dict_stack[-1]["get"] = ops.get_oper
    dict_stack[-1]["getinterval"] = ops.getinterval_oper
    dict_stack[-1]["putinterval"] = ops.putinterval_oper

    # stack operations
    dict_stack[-1]["exch"] = ops.exch_oper
    dict_stack[-1]["pop"] = ops.pop_oper
    dict_stack[-1]["copy"] = ops.copy_oper
    dict_stack[-1]["dup"] = ops.dup_oper
    dict_stack[-1]["clear"] = ops.clear_oper
    dict_stack[-1]["count"] = ops.count_oper

    # boolean operations
    dict_stack[-1]["eq"] = ops.eq_oper
    dict_stack[-1]["ne"] = ops.ne_oper
    dict_stack[-1]["ge"] = ops.ge_oper
    dict_stack[-1]["gt"] = ops.gt_oper
    dict_stack[-1]["le"] = ops.le_oper
    dict_stack[-1]["lt"] = ops.lt_oper
    dict_stack[-1]["and"] = ops.and_oper
    dict_stack[-1]["not"] = ops.not_oper
    dict_stack[-1]["or"] = ops.or_oper

    # flow control operations
    dict_stack[-1]["if"] = ops.if_oper