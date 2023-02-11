from hrd import Piece, Board, State, Solver, read_from_file
import pytest


def test_h_value():
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)


def test_f_value():
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)


def test_advanced_f_value():
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)


def test_get_path():
    infile = 'testhrd_easy1.txt'
    board = read_from_file(infile)


if __name__ == "__main__":
    pytest.main(['state_tests.py'])
