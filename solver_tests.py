from hrd import Piece, Board, State, Solver, read_from_file
from copy import deepcopy
import pytest


def test_dfs():
    pass


def test_a_star():
    pass


def test_generate_successors():
    pass


def test_move_single_piece_u():
    """

    """
    infile1 = 'Text files/test_e1_move_single_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_single_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (4, 2), (3, 2), 'u')
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
    new_board = solver.move_piece(successor_dict, (3, 2), (4, 2), 'd')
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
    new_board = solver.move_piece(successor_dict, (0, 3), (0, 2), 'l')
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
    new_board = solver.move_piece(successor_dict, (0, 2), (0, 3), 'r')
    assert new_board.bdict == board2.bdict


def test_move_ver_piece_u():
    infile1 = 'Text files/test_e1_move_ver_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_ver_d.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (2, 3), (0, 3), 'u', (1, 3), '^')
    assert new_board.bdict == board2.bdict


def test_move_ver_piece_d():
    infile1 = 'Text files/test_e1_move_ver_d.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_ver_u.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (0, 3), (2, 3), 'd', (3, 3), '^')
    assert new_board.bdict == board2.bdict


def test_move_ver_piece_l():
    infile1 = 'Text files/testhrd_easy1.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/test_e1_move_ver_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (3, 3), (3, 2), 'l', (4, 2), '^')
    assert new_board.bdict == board2.bdict


def test_move_ver_piece_r():
    infile1 = 'Text files/test_e1_move_ver_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/testhrd_easy1.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, (3, 2), (3, 3), 'r', (4, 3), '^')
    assert new_board.bdict == board2.bdict


def test_move_hor_piece():
    pass


if __name__ == "__main__":
    pytest.main(['solver_tests.py'])
