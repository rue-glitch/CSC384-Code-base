from csp import Constraint, Variable, CSP
from constraints import *
from backtracking import bt_search
from copy import deepcopy
import sys
import argparse


def print_solution(s, size):
    s_ = {}
    for (var, val) in s:
        s_[int(var.name())] = val
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            print(s_[-1 - (i * size + j)], end="")
        print('')


def read_solution(s, size):
    ship_count = 0
    sol = []
    s_ = {}
    for (var, val) in s:
        s_[int(var.name())] = val
    for i in range(1, size - 1):
        row = []
        for j in range(1, size - 1):
            row.append(s_[-1 - (i * size + j)])
            if s_[-1 - (i * size + j)] == 1:
                ship_count += 1
        sol.append(row)
    return sol, ship_count


# parse board and ships info
"""
parser = argparse.ArgumentParser()
parser.add_argument(
    "--inputfile",
    type=str,
    required=True,
    help="The input file that contains the puzzles."
)
parser.add_argument(
    "--outputfile",
    type=str,
    required=True,
    help="The output file that contains the solution."
)
args = parser.parse_args()
"""

#file = open(args.inputfile, 'r')
file = open('input_easy1.txt', 'r')
lines = file.readlines()
num_ship = lines[2].strip()
# num_ship is '3210'
# the number of submarines, destroyers, cruisers and battleships
total_num_ship = 0
ship_dict = {}
for i in range(len(num_ship)):
    if i == 0:
        ship_dict['S'] = int(num_ship[i])
        total_num_ship += int(num_ship[i])
    if i == 1:
        ship_dict['D'] = int(num_ship[i])
        total_num_ship += (int(num_ship[i]) * 2)
    if i == 2:
        ship_dict['C'] = int(num_ship[i])
        total_num_ship += (int(num_ship[i]) * 3)
    if i == 3:
        ship_dict['B'] = int(num_ship[i])
        total_num_ship += (int(num_ship[i]) * 4)
print(ship_dict)

#output_file = args.outputfile
output_file = 'output_1.txt'
#file = open(args.inputfile, 'r')
file = open('input_easy1.txt', 'r')
b = file.read()
b2 = b.split()
size = len(b2[0])
size = size + 2
b3 = []
b3 += ['0' + b2[0] + '0']
b3 += ['0' + b2[1] + '0']
b3 += [b2[2] + ('0' if len(b2[2]) == 3 else '')]
b3 += ['0' * size]
for i in range(3, len(b2)):
    b3 += ['0' + b2[i] + '0']
b3 += ['0' * size]
board = "\n".join(b3)

varlist = []
varn = {}
conslist = []

# 1/0 variables
for i in range(0, size):
    for j in range(0, size):
        v = None
        if i == 0 or i == size - 1 or j == 0 or j == size - 1:
            v = Variable(str(-1 - (i * size + j)), [0])
        else:
            v = Variable(str(-1 - (i * size + j)), [0, 1])
        varlist.append(v)
        varn[str(-1 - (i * size + j))] = v

# make 1/0 variables match board info
ii = 0
for i in board.split()[3:]:
    jj = 0
    for j in i:
        if j != '0' and j != '.':
            conslist.append(TableConstraint('boolean_match',
                                            [varn[str(-1 - (ii * size + jj))]],
                                            [[1]]))
        elif j == '.':
            conslist.append(TableConstraint('boolean_match',
                                            [varn[str(-1 - (ii * size + jj))]],
                                            [[0]]))
        jj += 1
    ii += 1

# row and column constraints on 1/0 variables
row_constraint = []
for i in board.split()[0]:
    row_constraint += [int(i)]

for row in range(0, size):
    conslist.append(NValuesConstraint('row',
                                      [varn[str(-1 - (row * size + col))] for
                                       col in range(0, size)], [1],
                                      row_constraint[row], row_constraint[row]))

col_constraint = []
for i in board.split()[1]:
    col_constraint += [int(i)]

for col in range(0, size):
    conslist.append(NValuesConstraint('col',
                                      [varn[str(-1 - (col + row * size))] for
                                       row in range(0, size)], [1],
                                      col_constraint[col], col_constraint[col]))

# diagonal constraints on 1/0 variables
for i in range(1, size - 1):
    for j in range(1, size - 1):
        for k in range(9):
            conslist.append(NValuesConstraint('diag',
                                              [varn[str(-1 - (i * size + j))],
                                               varn[str(-1 - ((i - 1) * size + (
                                                       j - 1)))]], [1], 0,
                                              1))
            conslist.append(NValuesConstraint('diag',
                                              [varn[str(-1 - (i * size + j))],
                                               varn[str(-1 - ((i - 1) * size + (
                                                       j + 1)))]], [1], 0,
                                              1))

# ./S/</>/v/^/M variables
# these would be added to the csp as well, before searching,
# along with other constraints
#for i in range(0, size):
#    for j in range(0, size):
#        v = Variable(str(i*size+j), ['.', 'S', '<', '^', 'v', 'M', '>'])
#        varlist.append(v)
#        varn[str(str(i*size+j))] = v
#        #connect 1/0 variables to W/S/L/R/B/T/M variables
#        conslist.append(TableConstraint('connect', [varn[str(-1-(i*size+j))], varn[str(i*size+j)]], [[0,'.'],[1,'S'],[1,'<'],[1,'^'],[1,'v'],[1,'M'],[1,'>']]))

# find all solutions and check which one has right ship #'s
csp = CSP('battleship', varlist, conslist)
# solutions, num_nodes = bt_search('BT', csp, 'mrv', True, False)
solutions, num_nodes = bt_search('GAC', csp, 'mrv', True, False)


def clean_ship(sol):
    # type is in ship_dict
    curr_ship_dict = deepcopy(ship_dict)
    result = [['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'],
              ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'],
              ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]
    for i in range(len(sol)):
        for j in range(len(sol[i])):
            if j == 5 and i == 5:
                print('yes')
            if sol[i][j] == 1 and j + 3 < len(sol[i]) and sol[i][j + 1] == 1 \
                    and sol[i][j + 2] == 1 and sol[i][j + 3] == 1 and \
                    curr_ship_dict['B'] > 0:
                # know it's a <M> -> battleship
                result[i][j] = '<'
                result[i][j + 1] = 'M'
                result[i][j + 2] = 'M'
                result[i][j + 3] = '>'
                curr_ship_dict['B'] -= 1
            elif sol[i][j] == 1 and i + 3 < len(sol) and sol[i + 1][j] == 1 \
                    and sol[i + 2][j] == 1 and sol[i + 3][j] == 1 and \
                    curr_ship_dict['B'] > 0:
                result[i][j] = '^'
                result[i + 1][j] = 'M'
                result[i + 2][j] = 'M'
                result[i + 3][j] = 'v'
                curr_ship_dict['B'] -= 1
            elif sol[i][j] == 1 and j + 2 < len(sol[i]) and sol[i][j + 1] == 1 \
                    and sol[i][j + 2] == 1 and curr_ship_dict['C'] > 0:
                # know it's a <M> -> cruiser
                result[i][j] = '<'
                result[i][j + 1] = 'M'
                result[i][j + 2] = '>'
                curr_ship_dict['C'] -= 1
            elif sol[i][j] == 1 and i + 2 < len(sol) and sol[i + 1][j] == 1 \
                    and sol[i + 2][j] == 1 and curr_ship_dict['C'] > 0:
                result[i][j] = '^'
                result[i + 1][j] = 'M'
                result[i + 2][j] = 'v'
                curr_ship_dict['C'] -= 1
            elif sol[i][j] == 1 and j + 1 < len(sol[i]) and sol[i][j + 1] == 1 \
                    and curr_ship_dict['D'] > 0 and result[i][j] == '.':
                # know it's a <> -> destroyer
                result[i][j] = '<'
                result[i][j + 1] = '>'
                curr_ship_dict['D'] -= 1
            elif sol[i][j] == 1 and i + 1 < len(sol) and sol[i + 1][j] == 1 \
                    and curr_ship_dict['D'] > 0 and result[i][j] == '.':
                result[i][j] = '^'
                result[i + 1][j] = 'v'
                curr_ship_dict['D'] -= 1
            elif sol[i][j] == 1 and j + 1 < len(sol[i]) and i + 1 < len(sol) \
                    and sol[i + 1][j] == 0 and sol[i][j + 1] == 0 \
                    and curr_ship_dict['S'] > 0 and result[i][j] == '.':
                result[i][j] = 'S'
                curr_ship_dict['S'] -= 1
            elif sol[i][j] == 1 and curr_ship_dict['S'] > 0 and result[i][
                j] == '.':
                result[i][j] = 'S'
                curr_ship_dict['S'] -= 1
    return result, curr_ship_dict


def write_to_file(filename, result):
    file = open(filename, 'w')
    for row in result:
        # row 1
        string = ''.join(row)
        file.write(string)
        file.write("\n")


for i in range(len(solutions)):
    print_solution(solutions[i], size)
    print("--------------")
    sol, ship_count = read_solution(solutions[i], size)
    if ship_count == total_num_ship:
        result, cleaned_dict = clean_ship(sol)
        cleaned_dict_list = list(cleaned_dict.values())
        cleaned_dict_values = 0
        for val in cleaned_dict_list:
            cleaned_dict_values += val
        if cleaned_dict_values == 0:
            write_to_file(output_file, result)
            break




