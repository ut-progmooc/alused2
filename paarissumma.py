from rattad import *
from grader import *


FUNCTION_NAME = 'paarissumma'


def solution(n):
    return sum(range(0, int(n/2)*2+1, 2))


def gen_test(test_arg, function_name):
    @test
    @expose_ast
    @set_description('Argument: {}'.format(test_arg))
    def do_test(m, AST):
        must_not_have_input(AST)

        # check correctness of definition
        must_have_func_def_toplevel(m.module, function_name)
        actual_func_node = get_function_def_node(AST, function_name)
        must_have_n_params(actual_func_node, 1)
        must_have_recursive_function_call(actual_func_node, function_name)

        # check return value correctness
        actual_func_obj = get_function(m.module, function_name)
        must_have_equal_return_values(solution, actual_func_obj, function_name, test_arg, ret_representer=quote)


gen_test(1, FUNCTION_NAME)
gen_test(2, FUNCTION_NAME)
gen_test(3, FUNCTION_NAME)
gen_test(10, FUNCTION_NAME)
gen_test(100, FUNCTION_NAME)
