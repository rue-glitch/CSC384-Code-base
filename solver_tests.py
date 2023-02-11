from hrd import Piece, Board, State, Solver, read_from_file
from copy import deepcopy
import pytest


def test_dfs():
    infile1 = 'Text files/testhrd_easy1.txt'
    board1 = read_from_file(infile1)
    solver = Solver()
    path, g = solver.dfs_solve(board1)
    print(path)
    assert path is not None


def test_dfs_2():
    infile1 = 'Text files/Board tests/board3.txt'
    board1 = read_from_file(infile1)
    solver = Solver()
    path, g = solver.dfs_solve(board1)
    print(path)
    assert path is not None


def test_a_star():
    pass


if __name__ == "__main__":
    pytest.main(['solver_tests.py'])
