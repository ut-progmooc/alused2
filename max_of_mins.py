from grader import *
from random import randint
from rattad import *


def solution(mat):
    return max([min(row) for row in mat])


def random_matrix():
    rows = randint(1, 10)
    cols = randint(1, 5)
    result = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(randint(-10, 10))
        result.append(row)
    return result



FUNCTION_NAME = 'vahimatest_suurim'

def gen_test(test_arg, function_name, desc):

    @test
    @expose_ast
    @set_description(desc)
    def do_test(m, AST):
        must_not_have_input(AST)

        must_have_func_def_toplevel(m.module, function_name)
        actual_func_node = get_function_def_node(AST, function_name)
        must_have_n_params(actual_func_node, 1)

        actual_func_obj = get_function(m.module, function_name)
        must_have_equal_return_values(solution, actual_func_obj, function_name, test_arg, args_repr=matrix_repr(test_arg))



a = [[1, 2],
     [1, 0]]
gen_test(a, FUNCTION_NAME, 'Lihtne maatriks 1')

b = [[-1, 9],
     [5, -1],
     [-1, 1]]
gen_test(b, FUNCTION_NAME, 'Lihtne maatriks 2')

c = [[1, 9],
     [5, 1],
     [2, 2],
     [3, 6]]
gen_test(c, FUNCTION_NAME, 'Keerulisem maatriks 1')

d = [[1, 0, -9001]]
gen_test(d, FUNCTION_NAME, 'Keerulisem maatriks 2')

e = [[42]]
gen_test(e, FUNCTION_NAME, 'Üheelemendiline maatriks')

for i in range(10):
    gen_test(random_matrix(), FUNCTION_NAME, 'Juhuslik maatriks {}'.format(i))

