from hrd import Piece, Board, State, Solver, read_from_file
from copy import deepcopy
import pytest


def test_find_shor_piece_l():
    infile1 = 'Text files/Movement tests/test_e1_move_shor_l.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_shor_r.txt'
    board2 = read_from_file(infile2)
    state = State(board1, 0)
    solver = Solver()
    # find_move_piece(self, state, single_piece_types, empty_key)
    single_piece_types = {
        '2': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        '<': [(0, -2), (0, 1)],
        '^': [(-2, 0), (1, 0)]
    }
    temp = solver.find_move_piece(state, single_piece_types, (2, 0))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_find_shor_piece_r():
    infile1 = 'Text files/Movement tests/test_e1_move_shor_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_shor_l.txt'
    board2 = read_from_file(infile2)
    state = State(board1, 0)
    solver = Solver()
    # find_move_piece(self, state, single_piece_types, empty_key)
    single_piece_types = {
        '2': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        '<': [(0, -2), (0, 1)],
        '^': [(-2, 0), (1, 0)]
    }
    temp = solver.find_move_piece(state, single_piece_types, (2, 2))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_move_shor_piece_l():
    infile1 = 'Text files/Movement tests/test_e1_move_shor_l.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_shor_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    # move_single_vertical_piece(self, bdict, move_key, empty_key)
    # find_move_piece(self, state, d, single_piece_types, empty_key)
    new_board = solver.move_single_horizontal_piece(successor_dict, (2, 1), (2, 0))
    assert new_board.bdict == board2.bdict


def test_move_shor_piece_r():
    infile1 = 'Text files/Movement tests/test_e1_move_shor_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_shor_l.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    # move_single_vertical_piece(self, bdict, move_key, empty_key)
    new_board = solver.move_single_horizontal_piece(successor_dict, (2, 0), (2, 2))
    assert new_board.bdict == board2.bdict


def test_move_hor_piece_u():
    """
    move_piece(self, successor_dict, pchar, move_key, empty_key_1,
                   empty_key_2=None, orientation=None)
    """
    infile1 = 'Text files/Movement tests/test_e1_move_hor_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_hor_d.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    block_piece_types = {
        '^': [(0, -1), (0, 1)],
        '<': [(1, 0), (-1, 0)],
        '1': [(2, 0), (1, 0), (0, -2), (0, 1)]
    }
    state = State(board1, 0)
    temp = solver.find_block_piece(state, block_piece_types, 'h', (2, 2), (2, 3))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_move_hor_piece_d():
    """

    """
    infile1 = 'Text files/Movement tests/test_e1_move_hor_d.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_hor_u.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    block_piece_types = {
        '^': [(0, -1), (0, 1)],
        '<': [(1, 0), (-1, 0)],
        '1': [(2, 0), (1, 0), (0, -2), (0, 1)]
    }
    state = State(board1, 0)
    temp = solver.find_block_piece(state, block_piece_types, 'h',  (3, 2), (3, 3))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_move_hor_piece_l():
    infile1 = 'Text files/Movement tests/test_e1_move_hor_l.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_hor_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    new_board = solver.move_single_horizontal_piece(board1.bdict, (2, 0), (2, 2))
    assert new_board.bdict == board2.bdict


def test_move_hor_piece_r():
    infile1 = 'Text files/Movement tests/test_e1_move_hor_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_hor_l.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    new_board = solver.move_single_horizontal_piece(board1.bdict, (2, 1), (2, 0))
    assert new_board.bdict == board2.bdict


if __name__ == "__main__":
    pytest.main(['horizontal_mov_tests.py'])
