from checkers import read_from_file, Board
import pytest


def test_b_movements():
    filename = 'b_movements.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    moves = board.get_piece_moves('b', (1, 4))
    print(moves)
    # move up left
    assert (2, 3) in moves.keys() and moves[(2, 3)] == []
    # move up right
    assert (2, 5) in moves.keys() and moves[(2, 5)] == []


def test_b_king_movements():
    filename = 'b_movements.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    moves = board.get_piece_moves('B', (6, 4))
    print(moves)
    # move down -> failing in moving down
    assert (7, 3) in moves.keys() and moves[(7, 3)] == []
    assert (7, 5) in moves.keys() and moves[(7, 5)] == []
    # move up
    assert (5, 5) in moves.keys() and moves[(5, 5)] == []
    assert (5, 3) in moves.keys() and moves[(5, 3)] == []




