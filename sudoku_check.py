from random import randint, shuffle, choice

from grader import *
from rattad import *

CORRECT_ANS = 'OK'
INCORRECT_ANS = 'VIGA'


def solution(mat):
    def rows():
        for row in mat:
            if len(set(row)) != len(row):
                return False
        return True
    def cols():
        for j in range(len(mat[0])):
            col = []
            for row in mat:
                col.append(row[j])
            if len(set(col)) != len(col):
                return False
        return True
    def boxes():
        for rea_nurk in range(0, 9, 3):
            for veeru_nurk in range(0, 9, 3):
                kast = []
                for i in range(3):
                    for j in range(3):
                        kast.append(int(mat[rea_nurk+i][veeru_nurk+j]))
                if sorted(kast) != list(range(1, 10)):
                    return False
        return True

    return CORRECT_ANS if rows() and cols() and boxes() else INCORRECT_ANS



def random_sudoku(is_correct):
    sudokus = """534678912
    672195348
    198342567
    859761423
    426853791
    713924856
    961537284
    287419635
    345286179
    835416927
    296857431
    417293658
    569134782
    123678549
    748529163
    652781394
    981345276
    374962815
    357964281
    468123579
    912587463
    631795842
    724318695
    895246137
    176459328
    583672914
    249831756
    846792315
    217435896
    593681274
    658917423
    371248569
    429356781
    964873152
    735129648
    182564937
    149275638
    573618924
    862349517
    495732861
    786591342
    321486795
    238167459
    617954283
    954823176
    256378941
    134569278
    798214365
    379156824
    615842739
    482793156
    867431592
    923685417
    541927683"""

    sudokus = sudokus.split()
    l = len(sudokus)

    random_sudoku = randint(0, l / 9 - 1)
    start = random_sudoku * 9
    end = start + 9
    sudoku = []

    while start < end:
        sudoku.append(sudokus[start])
        start += 1

    rowblocks = []

    def make_block(n, list):
        return [list[i] for i in range(n, n + 3)]

    rowblocks.append(make_block(0, sudoku))
    rowblocks.append(make_block(3, sudoku))
    rowblocks.append(make_block(6, sudoku))

    # Shuffle row blocks
    shuffle(rowblocks)

    # Shuffle rows inside blocks
    for i in range(3):
        shuffle(rowblocks[i])

    def remove_blocks(blocks):
        return [block[n] for block in blocks for n in range(3)]

    sudoku = remove_blocks(rowblocks)

    # Create columns
    columns = []
    for i in range(9):
        col = []
        for row in sudoku:
            col.append(row[i])
        col = "".join(col)
        columns.append(col)

    colblocks = []

    colblocks.append(make_block(0, columns))
    colblocks.append(make_block(3, columns))
    colblocks.append(make_block(6, columns))

    # Shuffle column blocks
    shuffle(colblocks)

    # Switch columns inside blocks
    for i in range(3):
        shuffle(colblocks[i])

    # Over to rows again
    columns = remove_blocks(colblocks)
    rows = []
    for i in range(9):
        row = []
        for col in columns:
            row.append(col[i])
        row = "".join(row)
        rows.append(row)

    # Switch two numbers inside sudoku
    sudoku = []
    a = randint(1, 9)
    b = randint(1, 9)
    while b == a:
        b = randint(1, 9)
    for row in rows:
        row = list(row)
        a = str(a)
        b = str(b)
        i1 = row.index(a)
        i2 = row.index(b)
        row[i1] = b
        row[i2] = a
        sudoku.append(row)

    # For an incorrect sudoku replace a random number with another number
    if not is_correct:
        numbers = [i for i in range(1, 10)]
        i = randint(0, 8)
        j = randint(0, 8)
        numbers.remove(int(sudoku[i][j]))
        sudoku[i][j] = str(numbers[randint(0, 7)])

    sudoku = "\n".join([" ".join(sudoku[i]) for i in range(9)])
    return sudoku


def gen_test(filename, matrix_str, desc):
    matrix = list(map(lambda r: r.split(' '), matrix_str.split('\n')))

    @test
    @expose_ast
    @set_description(desc)
    @create_temporary_file(filename, matrix_str)
    def do_test(m, AST):
        must_have_input(AST)

        expected_out = solution(matrix)
        unexpected_out = CORRECT_ANS if expected_out == INCORRECT_ANS else INCORRECT_ANS

        must_have_correct_output_str(m.stdin, m.stdout, [filename], [expected_out], [unexpected_out])


gen_test('naitefail_korrektne.txt', '''3 2 7 4 8 1 6 5 9
1 8 9 3 6 5 7 2 4
6 5 4 2 7 9 8 1 3
7 9 8 1 3 2 5 4 6
5 6 3 9 4 7 2 8 1
2 4 1 6 5 8 3 9 7
8 1 2 7 9 3 4 6 5
4 7 5 8 1 6 9 3 2
9 3 6 5 2 4 1 7 8''', 'Näitefail (korrektne)')

gen_test('naitefail_vigane.txt', '''3 2 7 4 8 1 6 5 9
1 8 9 3 6 5 7 2 4
6 5 4 2 7 9 8 1 3
7 9 8 1 3 2 5 4 6
5 6 3 9 4 7 2 8 1
1 4 1 6 5 8 3 9 7
8 1 2 7 9 3 4 6 5
4 7 5 8 1 6 9 3 2
9 3 6 5 2 4 1 7 8''', 'Näitefail (vigane)')

for i in range(1, 14):
    gen_test('juhuslik_sudoku_tabel.txt', random_sudoku(choice([True, False])), 'Juhuslik Sudoku tabel {}'.format(i))
