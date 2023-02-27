from checkers import read_from_file, Board
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


def test_r_king_movements():
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
    assert (5, 7) in moves.keys() and moves[(5, 7)] == []




