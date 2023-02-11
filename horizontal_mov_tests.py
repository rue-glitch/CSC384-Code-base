from hrd import Piece, Board, State, Solver, read_from_file
from copy import deepcopy
import pytest


def test_move_hor_piece_u():
    """

    """
    infile1 = 'Text files/test_e1_move_hor_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_hor_d.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (3, 2), (2, 2), (2, 3), '<')
    assert new_board.bdict == board2.bdict


def test_move_hor_piece_d():
    """

    """
    infile1 = 'Text files/test_e1_move_hor_d.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_hor_u.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (2, 2), (3, 2), (3, 3), '<')
    assert new_board.bdict == board2.bdict


def test_move_hor_piece_l():
    infile1 = 'Text files/test_e1_move_hor_l.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_hor_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (2, 0), (2, 2), (2, 3), '<')
    assert new_board.bdict == board2.bdict


def test_move_hor_piece_r():
    infile1 = 'Text files/test_e1_move_hor_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_hor_l.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (2, 2), (2, 0), (2, 1), '<')
    assert new_board.bdict == board2.bdict


if __name__ == "__main__":
    pytest.main(['horizontal_mov_tests.py'])
