from checkers import read_from_file, Board, Game
import pytest


def test_r_movements():
    filename = 'r_move_up.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    moves = board.get_piece_moves('r', (4, 6))
    print(moves)
    # move up left
    assert (3, 5) in moves.keys() and moves[(3, 5)] == []
    # move up right
    assert (3, 7) in moves.keys() and moves[(3, 7)] == []



    """def test_r_king_movements():
    filename = 'r_king_moves.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    moves = board.get_piece_moves('R', (4, 6))
    print(moves)
    # move up
    assert (3, 5) in moves.keys() and moves[(3, 5)] == []
    assert (3, 7) in moves.keys() and moves[(3, 7)] == []
    # ove down
    assert (5, 5) in moves.keys() and moves[(5, 5)] == []
    assert (5, 7) in moves.keys() and moves[(5, 7)] == []"""


def test_r_king_multi_jump():
    filename = 'r_king_moves.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    moves = board.get_piece_moves('R', (4, 6))
    print(moves)
    # multi jumps
    assert (0, 2) in moves.keys() and len(moves[(0, 2)]) == 2
    assert (0, 6) in moves.keys() and len(moves[(0, 6)]) == 2
    # move up
    assert (3, 7) in moves.keys() and moves[(3, 7)] == []
    # move down
    assert (5, 5) in moves.keys() and moves[(5, 5)] == []
    assert (5, 7) in moves.keys() and moves[(5, 7)] == []


def test_r_king_multi_jump_2():
    filename = 'r_king_moves.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    moves = board.get_piece_moves('R', (2, 6))
    print(moves)
    # multi jumps
    assert (4, 4) in moves.keys() and len(moves[(4, 4)]) == 1
    assert (0, 4) in moves.keys() and len(moves[(0, 4)]) == 1
    # move up
    assert (1, 7) in moves.keys() and moves[(1, 7)] == []
    # move down
    assert (3, 7) in moves.keys() and moves[(3, 7)] == []


def test_r_king_forced_capture():
    filename = 'r_king_moves.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    game = Game()
    moves = game.get_all_moves(board, 'r')
    print(moves)
    assert ((6, 3), 'r') in moves and len(moves[((6, 3), 'r')].keys()) == 2
    assert ((4, 1), 'r') in moves and len(moves[((4, 1), 'r')].keys()) == 1
    assert ((4, 6), 'R') in moves and len(moves[((4, 6), 'R')].keys()) == 2
    assert ((2, 6), 'R') in moves and len(moves[((2, 6), 'R')].keys()) == 2


