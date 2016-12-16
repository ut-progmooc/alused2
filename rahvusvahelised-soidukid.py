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


def failist_sõnastik(fname):
    d = {}
    with open(fname, encoding='utf-8') as f:
        for line in f.readlines():
            parts = line.strip().split()
            d[parts[0]] = parts[1]
    return d


def tähised_nimedeks(tahised, db):
    return list(map(lambda t: db[t] if t in db else None, tahised))


def solution(fname, tahised_str):
    d = failist_sõnastik(fname)
    nimed = tähised_nimedeks(tahised_str.split(), d)
    return '\n'.join(list(map(lambda x: 'Tundmatu maa' if x is None else x, nimed)))


def gen_test_f1(filename, file_content, desc):
    FUNCTION_NAME = 'failist_sõnastik'

    @test
    @expose_ast
    @set_description(desc)
    @create_temporary_file(filename, file_content)
    def do_test(m, AST):
        must_have_func_def_toplevel(m.module, FUNCTION_NAME)
        actual_func_node = get_function_def_node(AST, FUNCTION_NAME)
        must_have_n_params(actual_func_node, 1)

        actual_func_obj = get_function(m.module, FUNCTION_NAME)
        must_have_equal_return_values(failist_sõnastik, actual_func_obj, FUNCTION_NAME, filename, args_repr='oma faili nime "{}"'.format(filename))


def gen_test_f2(tahised, db, desc):
    FUNCTION_NAME = 'tähised_nimedeks'

    @test
    @expose_ast
    @set_description(desc)
    def do_test(m, AST):
        must_have_func_def_toplevel(m.module, FUNCTION_NAME)
        actual_func_node = get_function_def_node(AST, FUNCTION_NAME)
        must_have_n_params(actual_func_node, 2)

        actual_func_obj = get_function(m.module, FUNCTION_NAME)
        must_have_equal_return_values(tähised_nimedeks, actual_func_obj, FUNCTION_NAME, tahised, db, args_repr='järjendi {} ja sõnastiku {}'.format(tahised, db))


def gen_test(filename, file_content, tahised_str, desc):
    @test
    @expose_ast
    @set_description(desc)
    @create_temporary_file(filename, file_content)
    def do_test(m, AST):
        must_have_input(AST)
        must_have_correct_output_str(m.stdin, m.stdout, [filename, tahised_str], [solution(filename, tahised_str)], [])


naitefail = '''ER Eritrea
FIN Soome
F Prantsusmaa
H Ungari
LT Leedu
EST Eesti
S Rootsi'''
naitesonastik = {
    'ER': 'Eritrea',
    'FIN': 'Soome',
    'F': 'Prantsusmaa',
    'H': 'Ungari',
    'LT': 'Leedu',
    'EST': 'Eesti',
    'S': 'Rootsi'
}

teine_fail = '''EST Eesti
CY Küpros
'''
teine_sonastik = {
    'EST': 'Eesti',
    'CY': 'Küpros'
}

gen_test_f1('riigid.txt', naitefail, 'Esimene funktsioon näitefailiga')
gen_test_f1('baas.txt', teine_fail, 'Esimene funktsioon erineva failiga')

gen_test_f2(['S', 'EST', 'ARK', 'EST'], naitesonastik, 'Teine funktsioon näiteandmetega')
gen_test_f2(['S', 'EST', 'CY', 'FIN', 'FIN', 'EST'], teine_sonastik, 'Teine funktsioon erinevate andmetega')

gen_test('riigid.txt', naitefail, 'S EST ARK EST', 'Kogu programm näiteandmetega')
gen_test('baas.txt', teine_fail, 'S EST CY FIN FIN EST', 'Kogu programm erinevate andmetega')
