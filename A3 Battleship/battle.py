import argparse
import sys
from copy import copy, deepcopy
from csp import *
from constraints import *


class Board:
    """

    """

    def __init__(self, parent):
        self.parent = parent
        self.child = None
        self.row_constraints = []
        self.column_constraints = []
        self.num_ship = {}
        self.grid = []
        self.gdcit = {}


def fccheck(constraint, assignedvar, assignedval):
    var = constraint.unAssignedVars()[0]
    for val in var.curDomain():
        var.setValue(val)
        if not constraint.check():
            var.pruneValue(val, assignedvar, assignedval)
        # unassign val
        var.unAssign()
    if var.curDomainSize() == 0:
        return 'DWO'
    else:
        return 'OK'


SOLLIST = []


def fc(unassignedvars, csp):
    if unassignedvars.empty():
        # we found a solution
        # SOLLIST.append()
        for var in csp.variables:
            print(var.name(), ",", var.getValue())
            # print is the solution
            if allSolutions:
                return
            else:
                break
    var = unassignedvars.extract()
    for val in var.curDomain():
        var.setValue(val)
        noDWO = True
        for constraint in csp.constraintsOf(var):
            if constraint.numUnassigned() == 1:
                if fccheck(constraint, var, val) == 'DWO':
                    noDWO = False
                    break
        if noDWO:
            fc(unassignedvars, csp)
        var.restoreValues(var, val)
    var.setValue(None)
    unassignedvars.insert(var)
    return


def read_file(file):
    f = open(file)
    lines = f.readlines()
    var_list = []
    row_const = lines[0]
    col_const = lines[1]
    num_ship = lines[2]
    for row in range(len(lines[3:])):
        for col in range(len(lines[row])):
            if lines[row][col] is '0':
                domain = ('<', '>', '^', 'v', 'M', 'S', '.')
            else:
                domain = lines[row][col]
            var = Variable(str(row)+str(col), domain, row, col)
            var_list.append(var)
    return row_const, col_const, num_ship, var_list


if __name__ == '__main__':

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

    initial_board = read_file(args.inputfile)

    sys.stdout = open(args.outputfile, 'w')

    sys.stdout = sys.__stdout__
