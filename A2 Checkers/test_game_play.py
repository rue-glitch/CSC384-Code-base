from checkers import read_from_file, Board, Game, State
import math
import pytest


def test_get_children():
    filename = 'checkers2.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    state = State(board, 0)
    game = Game()
    children = game.get_children(state, 'r')
    for child in children:
        print(child.display())
    assert len(children) == 5


def test_game_play():
    filename = 'checkers2.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    state = State(board, 0)
    game = Game()
    # alphabeta_max_node(self, state, max_player, alpha, beta, current_depth)
    result = game.alphabeta(state, 10, True, -math.inf, +math.inf)
    #result = game.alphabeta_max_node(state, True, -math.inf, +math.inf, 12)
    print(result[1].display())
