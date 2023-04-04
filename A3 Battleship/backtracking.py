from csp import *
from constraints import *
import random


class UnassignedVars:
    '''class for holding the unassigned variables of a CSP. We can extract
       from, re-initialize it, and return variables to it.  Object is
       initialized by passing a select_criteria (to determine the
       order variables are extracted) and the CSP object.

       select_criteria = ['random', 'fixed', 'mrv'] with
       'random' == select a random unassigned variable
       'fixed'  == follow the ordering of the CSP variables (i.e.,
                   csp.variables()[0] before csp.variables()[1]
       'mrv'    == select the variable with minimum values in its current domain
                   break ties by the ordering in the CSP variables.
    '''

    def __init__(self, select_criteria, csp):
        if select_criteria not in ['random', 'fixed', 'mrv']:
            pass  # print "Error UnassignedVars given an illegal selection criteria {}. Must be one of 'random', 'stack', 'queue', or 'mrv'".format(select_criteria)
        self.unassigned = list(csp.variables())
        self.csp = csp
        self._select = select_criteria
        if select_criteria == 'fixed':
            # reverse unassigned list so that we can add and extract from the back
            self.unassigned.reverse()

    def extract(self):
        if not self.unassigned:
            pass  # print "Warning, extracting from empty unassigned list"
            return None
        if self._select == 'random':
            i = random.randint(0, len(self.unassigned) - 1)
            nxtvar = self.unassigned[i]
            self.unassigned[i] = self.unassigned[-1]
            self.unassigned.pop()
            return nxtvar
        if self._select == 'fixed':
            return self.unassigned.pop()
        if self._select == 'mrv':
            nxtvar = min(self.unassigned, key=lambda v: v.curDomainSize())
            self.unassigned.remove(nxtvar)
            return nxtvar

    def empty(self):
        return len(self.unassigned) == 0

    def insert(self, var):
        if not var in self.csp.variables():
            pass  # print "Error, trying to insert variable {} in unassigned that is not in the CSP problem".format(var.name())
        else:
            self.unassigned.append(var)


def bt_search(algo, csp, variableHeuristic, allSolutions, trace):
    '''Main interface routine for calling different forms of backtracking search
       algorithm is one of ['BT', 'FC', 'GAC']
       csp is a CSP object specifying the csp problem to solve
       variableHeuristic is one of ['random', 'fixed', 'mrv']
       allSolutions True or False. True means we want to find all solutions.
       trace True of False. True means turn on tracing of the algorithm

       bt_search returns a list of solutions. Each solution is itself a list
       of pairs (var, value). Where var is a Variable object, and value is
       a value from its domain.
    '''
    varHeuristics = ['random', 'fixed', 'mrv']
    algorithms = ['BT', 'FC', 'GAC']

    # statistics
    bt_search.nodesExplored = 0

    if variableHeuristic not in varHeuristics:
        pass  # print "Error. Unknown variable heursitics {}. Must be one of {}.".format(
        # variableHeuristic, varHeuristics)
    if algo not in algorithms:
        pass  # print "Error. Unknown algorithm heursitics {}. Must be one of {}.".format(
        # algo, algorithms)

    uv = UnassignedVars(variableHeuristic, csp)
    Variable.clearUndoDict()
    for v in csp.variables():
        v.reset()
    if algo == 'BT':
        solutions = BT(uv, csp, allSolutions, trace)
    elif algo == 'FC':
        for cnstr in csp.constraints():
            if cnstr.arity() == 1:
                FCCheck(cnstr, None,
                        None)  # FC with unary constraints at the root
        solutions = FC(uv, csp, allSolutions, trace)
    elif algo == 'GAC':
        GacEnforce(csp.constraints(), None, None, csp)  # GAC at the root
        solutions = GAC(uv, csp, allSolutions, trace)

    return solutions, bt_search.nodesExplored


def BT(unAssignedVars, csp, allSolutions, trace):
    '''Backtracking Search. unAssignedVars is the current set of
       unassigned variables.  csp is the csp problem, allSolutions is
       True if you want all solutionss trace if you want some tracing
       of variable assignments tried and constraints failed. Returns
       the set of solutions found.

      To handle finding 'allSolutions', at every stage we collect
      up the solutions returned by the recursive  calls, and
      then return a list of all of them.

      If we are only looking for one solution we stop trying
      further values of the variable currently being tried as
      soon as one of the recursive calls returns some solutions.
    '''
    if unAssignedVars.empty():
        if trace:
            pass  # print "{} Solution Found".format(csp.name())
        soln = []
        for v in csp.variables():
            soln.append((v, v.getValue()))
        return [soln]  # each call returns a list of solutions found
    # bt_search.nodesExplored += 1
    solns = []  # so far we have no solutions recursive calls
    nxtvar = unAssignedVars.extract()
    if trace:
        pass  # print "==>Trying {}".format(nxtvar.name())
    for val in nxtvar.domain():
        if trace:
            pass  # print "==> {} = {}".format(nxtvar.name(), val)
        nxtvar.setValue(val)
        constraintsOK = True
        for cnstr in csp.constraintsOf(nxtvar):
            if cnstr.numUnassigned() == 0:
                if not cnstr.check():
                    constraintsOK = False
                    if trace:
                        pass  # print "<==falsified constraint\n"
                    break
        if constraintsOK:
            new_solns = BT(unAssignedVars, csp, allSolutions, trace)
            if new_solns:
                solns.extend(new_solns)
            if len(solns) > 0 and not allSolutions:
                break  # don't bother with other values of nxtvar
                # as we found a soln.
    nxtvar.unAssign()
    unAssignedVars.insert(nxtvar)
    return solns


def FCCheck(constraint, assignedvar, assignedval):
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


def FC(unassignedvars, csp, allSolutions, trace):
    if unassignedvars.empty():
        # we found a solution
        if allSolutions:
            soln = []
            for v in csp.variables():
                soln.append((v, v.getValue()))
            return [soln]
        else:
            exit()
    solns = []
    var = unassignedvars.extract()
    for val in var.curDomain():
        var.setValue(val)
        noDWO = True
        for constraint in csp.constraintsOf(var):
            if constraint.numUnassigned() == 1:
                if FCCheck(constraint, var, val) == 'DWO':
                    noDWO = False
                    break
        if noDWO:
            new_solns = FC(unassignedvars, csp, allSolutions, trace)
            if new_solns:
                solns.extend(new_solns)
            if len(solns) > 0 and not allSolutions:
                break  # don't bother with other values of nxtvar
                # as we found a soln.
        var.restoreValues(var, val)
    var.setValue(None)
    unassignedvars.insert(var)
    return solns


def GAC(unassignedvars, csp, allSolutions, trace):
    if unassignedvars.empty():
        # we found a solution
        if allSolutions:
            soln = []
            for v in csp.variables():
                soln.append((v, v.getValue()))
            return [soln]
        else:
            exit()
    solns = []
    var = unassignedvars.extract()
    for val in var.curDomain():
        var.setValue(val)
        noDWO = True
        if GacEnforce(csp.constraintsOf(var), var, val, csp) == 'DWO':
            noDWO = False
        if noDWO:
            new_solns = GAC(unassignedvars, csp, allSolutions, trace)
            if new_solns:
                solns.extend(new_solns)
            if len(solns) > 0 and not allSolutions:
                break
        var.restoreValues(var, val)
    var.setValue(None)
    unassignedvars.insert(var)
    return solns


def GacEnforce(cnstr, assignedvar, assignedval, csp):
    while cnstr:
        curr_cnstr = cnstr.pop()
        for var in curr_cnstr.scope():
            for val in var.curDomain():
                if not curr_cnstr.hasSupport(var, val):
                    var.pruneValue(val, assignedvar, assignedval)
                if var.curDomainSize() == 0:
                    return 'DWO'
                for recheck in csp.constraintsOf(var):
                    if recheck != curr_cnstr and recheck not in cnstr:
                        cnstr.append(recheck)
    return 'OK'
