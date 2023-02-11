from copy import deepcopy
from heapq import heappush, heappop
import time
import argparse
import sys

# ====================================================================================

goal_char = '1'
single_char = '2'
empty_char = '.'
hor_char = '<'
ver_char = '^'


class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_goal, coord_x, coord_y, ptype):
        """
        :param is_goal: True if the piece is the goal piece and False otherwise.
        :type is_goal: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param ptype: The type of the piece (one of '2', '1', 'v', 'h', '.'
        :type ptype: str
        """

        self.is_goal = is_goal
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.ptype = ptype

    def __repr__(self):
        return '{} {} {} {}'.format(self.is_goal, self.coord_x,
                                    self.coord_y, self.ptype)

    def print_attributes(self):
        """
        Prints attributes of the piece
        """
        print(self.is_goal, self.coord_x, self.coord_y, self.ptype)


class Board:
    """
    Board class for setting up the playing board.

    - The 2x2 piece is denoted by 1
    - The single pieces are denoted by 2
    - Horizontal piece: 1x2 is denoted by <>
    - Vertical piece: 1x2 is denoted by ^ on the top and v on the bottom
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = 5

        self.pieces = pieces
        self.bdict = {}

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()
        self.grid_to_dict()

    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = goal_char
                self.grid[piece.coord_y][piece.coord_x + 1] = goal_char
                self.grid[piece.coord_y + 1][piece.coord_x] = goal_char
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = goal_char
            elif piece.ptype == single_char:
                self.grid[piece.coord_y][piece.coord_x] = single_char
            else:
                if piece.ptype == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = hor_char
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.ptype == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = ver_char
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'

    def display(self):
        """
        Print out the current board.
        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()

    def grid_to_dict(self):
        """
        Converts the grid to dictionary representation
        """
        seen = set()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == single_char or self.grid[i][j] == hor_char\
                        or self.grid[i][j] == ver_char or \
                        self.grid[i][j] == empty_char:
                    self.bdict[(i, j)] = self.grid[i][j]
                if self.grid[i][j] == goal_char and self.grid[i][j] not in seen:
                    # it's the 2x2 piece
                    self.bdict[(i, j)] = goal_char
                    seen.add(self.grid[i][j])
        return self.bdict

    def get_empty_space(self):
        """
        Gets the two empty spaces in the board.
        """
        result = []
        for key in self.bdict:
            if self.bdict[key] == empty_char:
                result.append(key)
        if result[0][0] == result[1][0]:
            # know it's side by side
            result.append('h')
        if result[0][1] == result[1][1]:
            # know it's side by side
            result.append('v')
        return result

    def is_goal_board(self):
        """
        Return True if this Board is solved, False otherwise.
        """
        # check if the 2x2 piece is in the right position
        if (3, 1) not in self.bdict.keys():
            return False
        elif self.bdict[(3, 1)] == goal_char:
            return True


class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces.
    State has a Board and some extra information that is relevant to the search:
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, depth, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param f: The f value of current state.
        :type f: int
        :param depth: The depth of current state in the search tree.
        :type depth: int
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.depth = depth
        self.parent = parent
        self.id = hash(board)  # The id for breaking ties.
        if self.parent is None:
            self.g = 0
        else:
            self.g = self.parent.g + 1

    def h_value(self):
        """
        Keeps track of the state's heuristic value
        """
        key1 = (0, 0)  # initializing variable for each piece's key
        key2 = (3, 1)  # goal key
        for key in self.board.bdict:
            if self.board.bdict[key] == 1:
                key1 = key
        x1, x2 = key1[0], key2[0]
        y1, y2 = key1[1], key2[1]
        distance = abs(x1 - x2) + abs(y1 - y2)
        return distance

    def f_value(self):
        """
        Keeps track of the state's f value
        """
        h = self.h_value()
        return h + self.g

    def f_advanced(self):
        """
        Keeps track of the state's advanced f value
        """
        pass

    def get_path(self):
        pass


class Solver:
    """
    Solver class holds the puzzle solvers
    """

    def generate_successors(self, state, seen=None):
        """
        Generates a list of successors for the current state
        """
        if seen is None:
            seen = set()
        board = state.board
        d = state.depth
        states = []
        successor_dict = deepcopy(board.bdict)
        single_type = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # empty keys in order of l, r, u, d
        piece_types = {
            hor_char: [(2, 0, 3, 0), (-1, 0, -2, 0), (-1, 0, -1, 1), (1, 0, 1, 1)],
            ver_char: [(0, -1, 1, -1), (0, 1, 1, 1), (-1, 0, -2, 0), (1, 0, 2, 0)],
            }

        for key in board.bdict:
            x, y = key
            piece = board.bdict[key]
            if piece == single_char:
                for dx, dy in single_type:
                    if (x + dx, y + dy) in board.bdict and \
                            board.bdict[(x + dx, y + dy)] == empty_char:
                        new_board = self.move_piece(successor_dict, key,
                                                    (x + dx, y + dy))
                        state = State(new_board, d+1)
                        states.append(state)

            if piece in piece_types:
                for dx1, dy1, dx2, dy2 in piece_types[piece]:
                    key1 = (x + dx1, y + dy1)
                    key2 = (x + dx2, y + dy2)
                    if key1 in board.bdict and board.bdict[key1] == empty_char \
                            and key2 in board.bdict and \
                            board.bdict[key2] == empty_char:
                        new_board = self.move_piece(successor_dict, key, key1,
                                                      key2, piece)
                        state = State(new_board, d+1)
                        states.append(state)
        return states

    def move_piece(self, successor_dict, move_key, empty_key_1,
                   empty_key_2=None, ptype=None):
        x, y = move_key[0], move_key[1]
        successor_dict.pop(move_key)
        successor_dict.pop(empty_key_1)
        successor_dict[move_key] = empty_char
        if ptype == single_char or ptype is None:
            successor_dict[empty_key_1] = single_char
        if ptype != single_char and ptype is not None:
            successor_dict.pop(empty_key_2)
            if ptype == hor_char:
                successor_dict[empty_key_1] = hor_char
                successor_dict[(x, y + 1)] = empty_char
            if ptype == ver_char:
                successor_dict[empty_key_1] = ver_char
                successor_dict[(x + 1, y)] = empty_char
            if ptype == goal_char:
                successor_dict[empty_key_1] = goal_char
                # TODO: figure out movement
        new_pieces = self.successor_dict_to_pieces(successor_dict)
        new_board = Board(new_pieces)
        if new_board.bdict == successor_dict:
            return new_board

    @staticmethod
    def successor_dict_to_pieces(dictionary):
        pieces = []
        g_found = False
        for key in dictionary:
            x, y = key[0], key[1]
            char = dictionary[key]
            pieces, g_found = create_pieces_list(char, pieces, g_found, y, x)
        return pieces

    def dfs(self):
        pass

    def a_star(self):
        pass


def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    g_found = False

    for line in puzzle_file:

        for x, ch in enumerate(line):
            pieces, g_found = create_pieces_list(ch, pieces, g_found, x, line_index)
        line_index += 1

    puzzle_file.close()

    board = Board(pieces)

    return board


def create_pieces_list(char, pieces, g_found, x, y):
    if char == ver_char:  # found vertical piece
        pieces.append(Piece(False, x, y, 'v'))
    elif char == hor_char:  # found horizontal piece
        pieces.append(Piece(False, x, y, 'h'))
    elif char == single_char:
        pieces.append(Piece(False, x, y, single_char))
    elif char == goal_char and not g_found:
        pieces.append(Piece(True, x, y, goal_char))
        g_found = True
    elif char == empty_char:
        pieces.append(Piece(False, x, y, empty_char))
    return pieces, g_found


def write_output_file():
    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()

    # read the board from the file
    board1 = read_from_file(args.inputfile)
