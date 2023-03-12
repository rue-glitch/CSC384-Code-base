from checkers import read_from_file, Board, Game, State
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
    # move down
    assert (7, 3) in moves.keys() and moves[(7, 3)] == []
    assert (7, 5) in moves.keys() and moves[(7, 5)] == []
    # move up
    assert (5, 5) in moves.keys() and moves[(5, 5)] == []
    assert (5, 3) in moves.keys() and moves[(5, 3)] == []


def test_b_king_multi_jump():
    filename = 'r_king_moves.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    moves = board.get_piece_moves('B', (7, 4))
    print(moves)
    # multi-jump up left
    assert (3, 0) in moves.keys() and moves[(3, 0)] == [(4, 1), (6, 3)]
    # move up
    assert (6, 5) in moves.keys() and moves[(6, 5)] == []


def test_b_king_multi_jump_2():
    filename = 'b_movements.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    moves = board.get_piece_moves('B', (7, 4))
    print(moves)
    # multi-jump up left
    assert (3, 0) in moves.keys() and len(moves[(3, 0)]) == 2
    # move up
    assert (5, 6) in moves.keys() and len(moves[(5, 6)]) == 1


def test_b_king_forced_capture():
    filename = 'b_movements.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    game = Game()
    moves = game.get_all_moves(board, 'b')
    print(moves)
    assert ((3, 2), 'b') in moves and len(moves[((3, 2), 'b')]) == 1
    assert ((3, 4), 'b') in moves and len(moves[((3, 4), 'b')]) == 2
    assert ((7, 4), 'B') in moves and len(moves[((7, 4), 'B')]) == 2
    assert ((1, 4), 'B') in moves and len(moves[((1, 4), 'B')]) == 4






