from hrd import Piece, Board, State, Solver, read_from_file
import pytest


def test_grid_to_dict():
    """
    Test grid_to_dict() outputs right dictionary for given input
    """
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)
    bdict = board.grid_to_dict()
    correct_dict = {(0, 0): '2', (0, 2): '2', (0, 3): '2', (1, 0): '2',
                    (1, 2): '<', (2, 0): '<', (2, 2): '<', (3, 0): '1',
                    (3, 2): '.', (4, 2): '.', (0, 1): '^', (3, 3): '^'}
    assert bdict == correct_dict


def test_get_empty_space():
    pass


def is_goal_board():
    pass


if __name__ == "__main__":
    pytest.main(['program_tests.py'])
