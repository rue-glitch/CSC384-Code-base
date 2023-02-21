from hrd import Piece, Board, State, Solver, read_from_file, write_output_file
from copy import deepcopy
import pytest


def test_dfs():
    infile1 = 'board2.txt'
    board1 = read_from_file(infile1)
    solver = Solver()
    path, g = solver.dfs_solve(board1)
    print(path)
    assert path is not None


def test_a_star():
    infile1 = 'board2.txt'
    board1 = read_from_file(infile1)
    solver = Solver()
    path, g = solver.a_solve(board1)
    write_output_file('../Text files/Board tests/board2_output.txt', path)
    assert path is not None


if __name__ == "__main__":
    pytest.main(['solver_tests.py'])
