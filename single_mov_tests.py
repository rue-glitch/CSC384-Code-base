from hrd import Piece, Board, State, Solver, read_from_file
from copy import deepcopy
import pytest


def test_move_single_piece_u():
    """

    """
    infile1 = 'Text files/test_e1_move_single_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_single_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (4, 2), (3, 2))
    assert new_board.bdict == board2.bdict


def test_move_single_piece_d():
    """

    """
    infile1 = 'Text files/test_e1_move_single_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_single_u.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (3, 2), (4, 2))
    assert new_board.bdict == board2.bdict


def test_move_single_piece_l():
    """
    move_piece(self, successor_dict, move_key, empty_key_1, orientation,
                   empty_key_2=None, ptype=None)
    """
    infile1 = 'Text files/test_e1_move_single_r_output.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_single_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (0, 3), (0, 2))
    assert new_board.bdict == board2.bdict


def test_move_single_piece_r():
    """
    """
    infile1 = 'Text files/test_e1_move_single_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_single_r_output.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (0, 2), (0, 3))
    assert new_board.bdict == board2.bdict


if __name__ == "__main__":
    pytest.main(['single_mov_tests.py'])
