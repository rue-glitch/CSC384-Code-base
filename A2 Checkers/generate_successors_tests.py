from checkers import read_from_file, Board, Game, State
import pytest


def test_get_children_r():
    filename = 'r_king_moves.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    state = State(board, 0)
    game = Game()
    children = game.get_children(state, 'r')
    for child in children:
        print(child.display())
    assert len(children) == 7


def test_get_children_b():
    filename = 'b_movements.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    state = State(board, 0)
    game = Game()
    children = game.get_children(state, 'b')
    for child in children:
        print(child.display())
    assert len(children) == 9
