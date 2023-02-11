from hrd import Piece, Board, State, Solver, read_from_file
from copy import deepcopy
import pytest


def test_move_ver_piece_u():
    infile1 = 'Text files/test_e1_move_ver_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_ver_d.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (2, 3), (0, 3), (1, 3), '^')
    assert new_board.bdict == board2.bdict


def test_move_ver_piece_d():
    infile1 = 'Text files/test_e1_move_ver_d.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_ver_u.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (0, 3), (2, 3), (3, 3), '^')
    assert new_board.bdict == board2.bdict


def test_move_ver_piece_l():
    infile1 = 'Text files/testhrd_easy1.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_ver_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (3, 3), (3, 2), (4, 2), '^')
    assert new_board.bdict == board2.bdict


def test_move_ver_piece_r():
    infile1 = 'Text files/test_e1_move_ver_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/testhrd_easy1.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (3, 2), (3, 3), (4, 3), '^')
    assert new_board.bdict == board2.bdict


if __name__ == "__main__":
    pytest.main(['vertical_mov_tests.py'])
