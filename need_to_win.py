import random
from rattad import *
from grader import *













def general_vaja(of_what):
    return list(filter(lambda e: e != 'X', of_what))


def func_1_solution(tbl):
    return general_vaja([tbl[0][0], tbl[0][-1], tbl[-1][0], tbl[-1][-1]])


def func_2_solution(tbl):
    diag = []
    for i in range(len(tbl)):
        diag.append(tbl[i][i])
        if i != int(len(tbl) / 2):
            diag.append(tbl[i][4 - i])
    return general_vaja(diag)


def func_3_solution(tbl):
    els = []
    for row in tbl:
        for el in row:
            els.append(el)
    return general_vaja(els)


def rand_input():
    p = random.randint(0, 100)
    mat = [["" for _ in range(5)] for _ in range(5)]
    for j in range(5):
        nums = random.sample(range(15*j+1, 15*(j+1)), 5)
        nums[:int((5*p/100))] = ['X' for _ in range(int((5*p/100)))]
        random.shuffle(nums)
        for i in range(5):
            mat[i][j] = nums[i]
    return mat






def gen_test(matrix, function_name, solution_func, description):
    @test
    @expose_ast
    @set_description(description)
    def do_test(m, AST):
        must_not_have_input(AST)

        must_have_func_def_toplevel(m.module, function_name)

        actual_func_node = get_function_def_node(AST, function_name)
        must_have_n_params(actual_func_node, 1)

        actual_func_obj = get_function(m.module, function_name)
        must_have_equal_return_values(solution_func, actual_func_obj, function_name, matrix,
                                      equalizer=equal_list_no_order, ret_representer=quote, args_repr=matrix_repr(matrix))

FUNCTION_NAME_1 = "nurkademänguks_vaja"
FUNCTION_NAME_2 = "diagonaalidemänguks_vaja"
FUNCTION_NAME_3 = "täismänguks_vaja"


gen_test([[1, 30, 34, 55, "X"], [10, 16, "X", 50, 67], ["X", 20, 38, 48, 61], [4, 26, 43, 49, 70], ["X", 17, 33, 51, 66]], FUNCTION_NAME_1, func_1_solution, "Näiteandmed, {}".format(FUNCTION_NAME_1))
gen_test([["X", 30, 34, 55, "X"],[10, "X", 40, 50, 67],[5, 20, "X", 48, 61],[4, "X", 43, "X", 70],[15, 17, 33, 51, "X"]], FUNCTION_NAME_2, func_2_solution, "Näiteandmed, {}".format(FUNCTION_NAME_2))
gen_test([["X", 30, 34, 55, "X"],["X", "X", "X", "X", "X"],[5, 20, "X", 48, 61],["X", "X", "X", "X", "X"],[15, 17, 33, 51, "X"]], FUNCTION_NAME_3, func_3_solution, "Näiteandmed, {}".format(FUNCTION_NAME_3))


for i in range(10):
    gen_test(rand_input(), FUNCTION_NAME_1, func_1_solution, "Juhuslikud andmed {}, {}".format(i, FUNCTION_NAME_1))

for i in range(10):
    gen_test(rand_input(), FUNCTION_NAME_2, func_2_solution, "Juhuslikud andmed {}, {}".format(i, FUNCTION_NAME_2))

for i in range(10):
    gen_test(rand_input(), FUNCTION_NAME_3, func_3_solution, "Juhuslikud andmed {}, {}".format(i, FUNCTION_NAME_3))


