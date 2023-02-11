from hrd import Piece, Board, State, Solver, read_from_file
from copy import deepcopy
import pytest


def test_move_goal_piece_u():
    """
    move_piece(self, successor_dict, pchar, move_key, empty_key_1,
                   empty_key_2=None, orientation=None)
    """
    infile1 = 'Text files/Movement tests/test_e1_move_goal_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_goal_d.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, '1', (3, 0), (2, 0), (2, 1), '<')
    assert new_board.bdict == board2.bdict


def test_move_goal_piece_d():
    infile1 = 'Text files/Movement tests/test_e1_move_goal_d.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_goal_u.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, '1', (2, 0), (4, 0), (4, 1), '<')
    assert new_board.bdict == board2.bdict


def test_move_goal_piece_l():
    infile1 = 'Text files/Movement tests/test_e1_move_goal_l.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_goal_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, '1', (3, 1), (3, 0), (4, 0), '^')
    assert new_board.bdict == board2.bdict


def test_move_goal_piece_r():
    infile1 = 'Text files/Movement tests/test_e1_move_goal_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_goal_l.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    new_board = solver.move_piece(successor_dict, '1', (3, 0), (3, 2), (4, 2), '^')
    assert new_board.bdict == board2.bdict


if __name__ == "__main__":
    pytest.main(['goal_mov_tests.py'])
