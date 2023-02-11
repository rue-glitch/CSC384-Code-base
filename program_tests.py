from hrd import Piece, Board, State, Solver, read_from_file
import pytest


def test_read_file():
    """
    Test if the input file is read correctly.

    Passed
    """
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)
    grid = [['2', '^', '2', '2'], ['2', 'v', '<', '>'], ['<', '>', '<', '>'],
            ['1', '1', '.', '^'], ['1', '1', '.', 'v']]
    assert board.grid == grid


if __name__ == "__main__":
    pytest.main(['program_tests.py'])
