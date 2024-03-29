from hrd import State, Solver, read_from_file
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
    block_piece_types = {
        '^': [(0, -1), (0, 1)],
        '<': [(1, 0), (-1, 0)],
        '1': [(2, 0), (1, 0), (0, -2), (0, 1)]
    }
    state = State(board1, 0)
    temp = solver.find_block_piece(state, block_piece_types, 'h', (2, 0), (2, 1))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_move_goal_piece_d():
    infile1 = 'Text files/Movement tests/test_e1_move_goal_d.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_goal_u.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    block_piece_types = {
        '^': [(0, -1), (0, 1)],
        '<': [(1, 0), (-1, 0)],
        '1': [(-2, 0), (1, 0), (0, -2), (0, 1)]
    }
    state = State(board1, 0)
    temp = solver.find_block_piece(state, block_piece_types, 'h', (4, 0), (4, 1))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_move_goal_piece_l():
    infile1 = 'Text files/Movement tests/test_e1_move_goal_l.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_goal_r.txt'
    board2 = read_from_file(infile2)
    solver = Solver()
    block_piece_types = {
        '^': [(0, -1), (0, 1)],
        '<': [(1, 0), (-1, 0)],
        '1': [(2, 0), (1, 0), (0, -2), (0, 1)]
    }
    state = State(board1, 0)
    temp = solver.find_block_piece(state, block_piece_types, 'v', (3, 0), (4, 0))
    for item in temp:
        print(item.board.display())
    assert temp != []


def test_move_goal_piece_r():
    infile1 = 'Text files/Movement tests/test_e1_move_goal_r.txt'
    board1 = read_from_file(infile1)
    infile2 = 'Text files/Movement tests/test_e1_move_goal_l.txt'
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


if __name__ == "__main__":
    pytest.main(['goal_mov_tests.py'])
