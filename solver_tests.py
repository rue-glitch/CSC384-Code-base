from hrd import Piece, Board, State, Solver, read_from_file
from copy import deepcopy
import pytest


def test_dfs():
    pass


def test_a_star():
    pass


def test_generate_successors_1():
    infile1 = 'Text files/testhrd_easy1.txt'
    board1 = read_from_file(infile1)
    state = State(board1, 0)
    solver = Solver()
    states = solver.generate_successors(state)
    for state in states:
        print('/n')
        print(state.board.display())
    assert states is not None


def test_generate_successors_2():
    infile1 = 'Text files/Board tests/board2.txt'
    board1 = read_from_file(infile1)
    state = State(board1, 0)
    solver = Solver()
    states = solver.generate_successors(state)
    for state in states:
        print('/n')
        print(state.board.display())
    assert states is not None


def test_generate_successors_3():
    infile1 = 'Text files/Board tests/board3.txt'
    board1 = read_from_file(infile1)
    state = State(board1, 0)
    solver = Solver()
    states = solver.generate_successors(state)
    for state in states:
        print('/n')
        print(state.board.display())
    assert states is not None


def test_generate_successors_4():
    infile1 = 'Text files/Board tests/board4.txt'
    board1 = read_from_file(infile1)
    state = State(board1, 0)
    solver = Solver()
    states = solver.generate_successors(state)
    for state in states:
        print('/n')
        print(state.board.display())
    assert states is not None


if __name__ == "__main__":
    pytest.main(['solver_tests.py'])
