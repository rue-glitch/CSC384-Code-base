from checkers import read_from_file, Board
import pytest


def test_read_file():
    filename = 'checkers2.txt'
    result = read_from_file(filename)
    actual = [['.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', 'b', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', 'R'], ['.', '.', 'b', '.', 'b', '.', '.', '.'], ['.', '.', '.', 'b', '.', '.', '.', 'r'], ['.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', 'r', '.', '.', '.', '.'], ['.', '.', '.', '.', 'B', '.', '.', '.']]
    assert actual == result


def test_grid_to_dict():
    filename = 'checkers2.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    pdict = board.grid_to_dict(grid)
    for key in pdict['b']:
        assert key not in pdict['.']



def test_dict_to_grid():
    filename = 'checkers2.txt'
    grid = read_from_file(filename)
    board = Board(grid)
    pdict = board.grid_to_dict(grid)
    generated_grid = board.dict_to_grid(pdict)
    assert grid == generated_grid

