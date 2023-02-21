from hrd import State, Solver, read_from_file
import pytest


def test_move_single_piece_u():
    """

    """
    infile1 = 'Text files/Movement tests/test_e1_move_single_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_single_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    new_board = solver.move_single_piece(board1.bdict, (4, 2), (3, 2))
    assert new_board.bdict == board2.bdict


def test_move_single_piece_d():
    """

    """
    infile1 = 'Text files/Movement tests/test_e1_move_single_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_single_u.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    new_board = solver.move_single_piece(board1.bdict, (3, 2), (4, 2))
    assert new_board.bdict == board2.bdict


def test_move_single_piece_l():
    """
    move_piece(self, successor_dict, move_key, empty_key_1, orientation,
                   empty_key_2=None, ptype=None)
    """
    infile1 = 'Text files/Movement tests/test_e1_move_single_r_output.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_single_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    new_board = solver.move_single_piece(board1.bdict, (0, 3), (0, 2))
    assert new_board.bdict == board2.bdict


def test_move_single_piece_r():
    """
    """
    infile1 = 'Text files/Movement tests/test_e1_move_single_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_single_r_output.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    new_board = solver.move_single_piece(board1.bdict, (0, 2), (0, 3))
    assert new_board.bdict == board2.bdict


def test_find_single_piece_l():
    """
    move_piece(self, successor_dict, move_key, empty_key_1, orientation,
                   empty_key_2=None, ptype=None)
    """
    infile1 = 'Text files/Movement tests/test_e1_move_single_r_output.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_single_r.txt'
    board2 = read_from_file(infile2)
    state = State(board1, 0)
    solver = Solver()
    # find_move_piece(self, state, single_piece_types, empty_key)
    single_piece_types = {
        '2': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        '<': [(0, -2), (0, 1)],
        '^': [(-2, 0), (1, 0)]
    }
    temp = solver.find_move_piece(state, single_piece_types, (0, 2))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_find_single_piece_u():
    """

    """
    infile1 = 'Text files/Movement tests/test_e1_move_single_u.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_single_r.txt'
    board2 = read_from_file(infile2)
    state = State(board1, 0)
    solver = Solver()
    # find_move_piece(self, state, single_piece_types, empty_key)
    single_piece_types = {
        '2': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        '<': [(0, -2), (0, 1)],
        '^': [(-2, 0), (1, 0)]
    }
    temp = solver.find_move_piece(state, single_piece_types, (3, 2))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_find_single_piece_d():
    """

    """
    infile1 = 'Text files/Movement tests/test_e1_move_single_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_single_u.txt'
    board2 = read_from_file(infile2)
    state = State(board1, 0)
    solver = Solver()
    # find_move_piece(self, state, single_piece_types, empty_key)
    single_piece_types = {
        '2': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        '<': [(0, -2), (0, 1)],
        '^': [(-2, 0), (1, 0)]
    }
    temp = solver.find_move_piece(state, single_piece_types, (4, 2))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_find_single_piece_r():
    """
    """
    infile1 = 'Text files/Movement tests/test_e1_move_single_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_single_r_output.txt'
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


if __name__ == "__main__":
    pytest.main(['single_mov_tests.py'])
