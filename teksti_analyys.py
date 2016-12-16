import os
import os.path
import string
import random
from grader import *
if not os.path.isfile('rattad.py'):
    os.rename('rattad.hack', 'rattad.py')
try:
    from rattad import *
except ImportError:
    print(os.listdir("."))


def solution(s):
    d = {}
    for c in s:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1
    return d


def random_string(n):
    return ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(n)])


def gen_test(test_arg, desc):
    FUNCTION_NAME = 'sümbolite_sagedus'

    @test
    @expose_ast
    @set_description(desc)
    def do_test(m, AST):
        must_not_have_input(AST)

        must_have_func_def_toplevel(m.module, FUNCTION_NAME)
        actual_func_node = get_function_def_node(AST, FUNCTION_NAME)
        must_have_n_params(actual_func_node, 1)

        actual_func_obj = get_function(m.module, FUNCTION_NAME)
        must_have_equal_return_values(solution, actual_func_obj, FUNCTION_NAME, test_arg, args_repr=quotemark_repr(test_arg))


gen_test('', 'Tühi sõne')
gen_test('a', 'Sõne: "a"')
gen_test('aa', 'Sõne: "aa"')
gen_test('1;;@@1', 'Sõne: "1;;@@1"')
gen_test(random_string(3), 'Juhuslik sõne pikkusega 3')
gen_test(random_string(5), 'Juhuslik sõne pikkusega 5')
gen_test(random_string(10), 'Juhuslik sõne pikkusega 10')
gen_test(random_string(15), 'Juhuslik sõne pikkusega 15')
gen_test(random_string(20), 'Juhuslik sõne pikkusega 20')
gen_test(random_string(25), 'Juhuslik sõne pikkusega 25')
