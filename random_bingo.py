from grader import *
from rattad import *

n = 10
function_name = 'juhuslik_bingo'

def is_legal_return_value(tbl):
    return False not in [15 * i + 1 <= el <= 15 * (i + 1) for row in tbl for i, el in enumerate(row)]


@test
@expose_ast
@set_description('{} juhuslikku tabelit'.format(n))
def do_test(m, AST):
    must_not_have_input(AST)

    # check correctness of definition
    must_have_func_def_toplevel(m.module, function_name)
    actual_func_node = get_function_def_node(AST, function_name)
    must_have_n_params(actual_func_node, 0)

    # check return value correctness
    actual_func_obj = get_function(m.module, function_name)
    must_have_correct_random_return_value(actual_func_obj, function_name, [], is_legal_return_value, samples=n)
