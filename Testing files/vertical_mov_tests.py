from hrd import Piece, Board, State, Solver, read_from_file
from copy import deepcopy
import pytest


def test_find_sver_piece_d():
    infile1 = 'Text files/Movement tests/test_e1_move_sver_d.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_sver_u.txt'
    board2 = read_from_file(infile2)
    state = State(board1, 0)
    solver = Solver()
    # find_move_piece(self, state, single_piece_types, empty_key)
    single_piece_types = {
        '2': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        '<': [(0, -2), (0, 1)],
        '^': [(-2, 0), (1, 0)]
    }
    temp = solver.find_move_piece(state, single_piece_types, (2, 3))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_find_sver_piece_u():
    infile1 = 'Text files/Movement tests/test_e1_move_sver_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_sver_d.txt'
    board2 = read_from_file(infile2)
    state = State(board1, 0)
    solver = Solver()
    # find_move_piece(self, state, single_piece_types, empty_key)
    single_piece_types = {
        '2': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        '<': [(0, -2), (0, 1)],
        '^': [(-2, 0), (1, 0)]
    }
    temp = solver.find_move_piece(state, single_piece_types, (0, 3))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_move_sver_piece_d():
    infile1 = 'Text files/Movement tests/test_e1_move_sver_d.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_sver_u.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    successor_dict = deepcopy(board1.bdict)
    # move_single_vertical_piece(self, bdict, move_key, empty_key)
    new_board = solver.move_single_vertical_piece(successor_dict, (0, 3), (2, 3))
    assert new_board.bdict == board2.bdict


def test_move_sver_piece_u():
    infile1 = 'Text files/Movement tests/test_e1_move_sver_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_sver_d.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    # move_single_vertical_piece(self, bdict, move_key, empty_key)
    new_board = solver.move_single_vertical_piece(board1.bdict, (1, 3), (0, 3))
    assert new_board.bdict is not None
    assert board2.bdict is not None
    assert new_board.bdict == board2.bdict


def test_find_ver_piece_u():
    infile1 = 'Text files/Movement tests/test_e1_move_ver_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_ver_d.txt'
    board2 = read_from_file(infile2)
    state = State(board1, 0)
    solver = Solver()
    # find_move_piece(self, state, single_piece_types, empty_key)
    single_piece_types = {
        '2': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        '<': [(0, -2), (0, 1)],
        '^': [(-2, 0), (1, 0)]
    }
    temp = solver.find_move_piece(state, single_piece_types, (1, 3))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_find_ver_piece_d():
    infile1 = 'Text files/Movement tests/test_e1_move_ver_d.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_ver_u.txt'
    board2 = read_from_file(infile2)
    state = State(board1, 0)
    solver = Solver()
    # find_move_piece(self, state, single_piece_types, empty_key)
    single_piece_types = {
        '2': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        '<': [(0, -2), (0, 1)],
        '^': [(-2, 0), (1, 0)]
    }
    temp = solver.find_move_piece(state, single_piece_types, (3, 3))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_move_ver_piece_u():
    infile1 = 'Text files/Movement tests/test_e1_move_ver_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_ver_d.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    # state, block_piece_types, e_key_orientation,
    #                          empty_key1, empty_key2)
    new_board = solver.move_single_vertical_piece(board1.bdict, (2, 3), (0, 3))
    assert new_board.bdict is not None
    assert board2.bdict is not None
    assert new_board.bdict == board2.bdict


def test_move_ver_piece_d():
    infile1 = 'Text files/Movement tests/test_e1_move_ver_d.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_ver_u.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    new_board = solver.move_single_vertical_piece(board1.bdict, (1, 3), (3, 3))
    assert new_board.bdict == board2.bdict


def test_move_ver_piece_l():
    # find_block_piece(self, state, block_piece_types, e_key_orientation,
    #                          empty_key1, empty_key2)
    infile1 = 'Text files/testhrd_easy1.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_ver_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    block_piece_types = {
        '^': [(0, -1), (0, 1)],
        '<': [(1, 0), (-1, 0)],
        '1': [(2, 0), (1, 0), (0, -2), (0, 1)]
    }
    state = State(board1, 0)
    temp = solver.find_block_piece(state, block_piece_types, 'v', (3, 2), (4, 2))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_move_ver_piece_r():
    infile1 = 'Text files/Movement tests/test_e1_move_ver_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/testhrd_easy1.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    block_piece_types = {
        '^': [(0, -1), (0, 1)],
        '<': [(1, 0), (-1, 0)],
        '1': [(2, 0), (1, 0), (0, -2), (0, 1)]
    }
    state = State(board1, 0)
    temp = solver.find_block_piece(state, block_piece_types, 'v', (3, 3), (4, 3))
    for item in temp:
        print(item.board.display())
    assert temp != []


if __name__ == "__main__":
    pytest.main(['vertical_mov_tests.py'])
