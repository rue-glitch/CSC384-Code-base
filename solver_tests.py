from hrd import Piece, Board, State, Solver, read_from_file
import pytest


def test_dfs():
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)
    pass


def test_a_star():
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)
    pass


def test_generate_successors():
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)
    pass


def test_move_single_piece():
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)
    pass


def test_move_hor_piece():
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)
    pass


def test_move_ver_piece():
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)
    pass


def test_successor_dict_to_pieces():
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)
    pass


if __name__ == "__main__":
    pytest.main(['solver_tests.py'])
