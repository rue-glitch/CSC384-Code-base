from copy import deepcopy
from heapq import heappush, heappop
import time
import argparse
import sys

# ====================================================================================
from typing import Optional, Set

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
                if self.grid[i][j] == single_char or self.grid[i][j] == hor_char \
                        or self.grid[i][j] == ver_char or \
                        self.grid[i][j] == empty_char:
                    self.bdict[(i, j)] = self.grid[i][j]
                if self.grid[i][j] == goal_char and self.grid[i][j] not in seen:
                    # it's the 2x2 piece
                    self.bdict[(i, j)] = goal_char
                    seen.add(self.grid[i][j])
        return self.bdict

    def get_empty_space(self) -> list:
        """
        Gets the two empty spaces in the board.
        """
        result = []
        for key in self.bdict:
            if self.bdict[key] == empty_char:
                result.append(key)
        return result

    def is_goal_board(self) -> bool:
        """
        Return True if this Board is solved, False otherwise.
        """
        # check if the 2x2 piece is in the right position
        if (3, 1) not in self.bdict.keys():
            return False
        elif self.bdict[(3, 1)] == goal_char:
            return True

    def str_rep(self):
        """
        Returns a string representation of board
        """
        str_rep = ''
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                str_rep += self.grid[i][j]
        return str_rep


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
        state = self
        path = []
        while state:
            path.append(state.board.str_rep())
            state = state.parent
        path.reverse()
        return path


class Solver:
    """
    Solver class holds the puzzle solvers
    """

    def __init__(self):
        self.frontier = []

    def dfs_solve(self, board: Board,
                  seen: Optional[Set[str]] = None):
        """
        Implement frontier approach to dfs
        """
        # adds initial state to the frontier
        seen = set()
        self.frontier.append(State(board, 0))
        while len(self.frontier):
            curr = self.frontier.pop()
            if curr.board.str_rep() not in seen:
                seen.add(curr.board.str_rep())
                if curr.board.is_goal_board():
                    path = curr.get_path()
                    return path, curr.g
                successors = self.generate_successors(curr, seen)
                print(curr.board.str_rep(), curr.depth)
                for successor in successors:
                    print(successor.board.str_rep())
                    #print(successor.board.display())
                #input("Press Enter to continue...")
                for successor in successors:
                    self.frontier.append(successor)

    def a_solve(self, board, seen: Optional = None):
        state = State(board, 0)
        f = state.f_value()
        entry = 0
        # 1. g(n) -> total cost of the states until that point
        # 2. h(n) -> is the estimated cost of only the 2x2 piece
        # 3. f(n) -> sum of h(n) and g(n)
        heap_piece = (f, entry, state)
        heappush(self.frontier, heap_piece)
        seen = set()
        while len(self.frontier):
            curr = heappop(self.frontier)
            board = curr[2].board
            if board.str_rep() not in seen:
                seen.add(board.str_rep())
                if board.is_goal_board():
                    # need to figure out how to clean the puzzle
                    path = curr[2].get_path()
                    return path, curr[2].g
                print(curr[2].board.str_rep(), curr[2].depth)
                successors = self.generate_successors(curr[2], seen)
                for successor in successors:
                    print(successor.board.display())
                    #input("Press Enter to continue...")
                for successor in successors:
                    if successor.board.str_rep() not in seen:
                        f = successor.f_value()
                        entry += 1
                        tup = (f, entry, successor)
                        heappush(self.frontier, tup)


        # 4. each state gets added into the heap and sorted based on f value
        # 5. pop the smallest state and explore it's successors
        # 6. assign each successor a f value and put it back in heap
        # 7. continue till solution

    def generate_successors(self, state, seen):
        """
        Generates a list of successors for the current state
        """
        board = state.board
        d = state.depth

        states = []
        single_piece_types = {
            single_char: [(1, 0), (-1, 0), (0, 1), (0, -1)],
            hor_char: [(0, -2), (0, 1)],
            ver_char: [(-2, 0), (-1, 0), (1, 0)]
        }
        block_piece_types = {
            ver_char: [(0, -1), (0, 1)],
            hor_char: [(1, 0), (-1, 0)],
            goal_char: [(2, 0), (1, 0), (0, -2), (0, 1)]
        }

        empty_keys = board.get_empty_space()
        empty_key1 = empty_keys[0]
        empty_key2 = empty_keys[1]
        e_key_orientation = None
        if empty_keys[0][0] == empty_keys[1][0] and abs(
                int(empty_keys[0][1]) - int(empty_keys[1][1])) == 1:
            # know it's side by side
            e_key_orientation = 'h'
        elif empty_keys[0][1] == empty_keys[1][1] and abs(
                int(empty_keys[0][0]) - int(empty_keys[1][0])) == 1:
            # know it's side by side
            e_key_orientation = 'v'
        print('e1')
        temp = self.find_move_piece(state, single_piece_types, empty_key1)
        for item in temp:
            if item.board.str_rep() not in seen:
                states.append(item)
        print('e2')
        temp1 = self.find_move_piece(state, single_piece_types, empty_key2)
        for item in temp1:
            if item.board.str_rep() not in seen:
                states.append(item)

        temp2 = self.find_block_piece(state, block_piece_types,
                                      e_key_orientation, empty_key1, empty_key2)
        for item in temp2:
            if item.board.str_rep() not in seen:
                states.append(item)

        return states

    def find_move_piece(self, state, single_piece_types, empty_key):
        board = state.board
        temp_states = []
        x, y = empty_key
        for key in single_piece_types.keys():
            for dx, dy in single_piece_types[key]:
                move_key = (x + dx, y + dy)
                if move_key in board.bdict:
                    if board.bdict[move_key] == single_char:
                        new_board = self.move_single_piece(board.bdict, move_key,
                                                           empty_key)
                        if new_board is not None:
                            new_state = State(new_board, state.depth + 1, state)
                            temp_states.append(new_state)
                    if board.bdict[move_key] == hor_char:
                        new_board = self.move_single_horizontal_piece(board.bdict, move_key,
                                                           empty_key)
                        if new_board is not None:
                            new_state = State(new_board, state.depth + 1, state)
                            temp_states.append(new_state)
                    if board.bdict[move_key] == ver_char:
                        new_board = self.move_single_vertical_piece(board.bdict, move_key,
                                                           empty_key)
                        if new_board is not None:
                            new_state = State(new_board, state.depth + 1, state)
                            temp_states.append(new_state)
        return temp_states

    def move_single_piece(self, bdict, move_key, empty_key):
        successor_dict = deepcopy(bdict)
        successor_dict.pop(move_key)
        successor_dict.pop(empty_key)
        successor_dict[move_key] = empty_char
        successor_dict[empty_key] = single_char
        new_pieces = self.successor_dict_to_pieces(successor_dict)
        new_board = Board(new_pieces)
        if new_board is not None:
            return new_board

    def move_single_vertical_piece(self, bdict, move_key, empty_key):
        successor_dict = deepcopy(bdict)
        x, y = move_key[0], move_key[1]
        successor_dict.pop(move_key)
        successor_dict.pop(empty_key)
        if x + 2 == empty_key[0]:
            # empty piece is at the bottom
            successor_dict[(x + 1, y)] = ver_char
            successor_dict[move_key] = empty_char
        elif x - 1 == empty_key[0]:
            # empty piece is at the top
            successor_dict[(x - 1, y)] = ver_char
            successor_dict[(x + 1, y)] = empty_char
        elif x - 2 == empty_key[0] and bdict[(1, 3)] == empty_char:
            # empty piece is at the top
            successor_dict[(x - 1, y)] = ver_char
            successor_dict[empty_key] = empty_char
        new_pieces = self.successor_dict_to_pieces(successor_dict)
        new_board = Board(new_pieces)
        if new_board is not None:
            return new_board

    def move_single_horizontal_piece(self, bdict, move_key, empty_key):
        successor_dict = deepcopy(bdict)
        x, y = move_key[0], move_key[1]
        successor_dict.pop(move_key)
        successor_dict.pop(empty_key)
        if y + 2 == empty_key[1]:
            # empty piece is at the left
            successor_dict[(x, y + 1)] = hor_char
            successor_dict[move_key] = empty_char
        elif y - 1 == empty_key[1]:
            # empty piece is at the top
            successor_dict[(x, y - 1)] = hor_char
            successor_dict[(x, y + 1)] = empty_char
        new_pieces = self.successor_dict_to_pieces(successor_dict)
        new_board = Board(new_pieces)
        if new_board is not None:
            return new_board

    def find_block_piece(self, state, block_piece_types, e_key_orientation,
                         empty_key1, empty_key2):
        board = state.board
        temp_states = []
        x, y = empty_key1

        for key in block_piece_types.keys():
            for dx, dy in block_piece_types[key]:
                move_key = (x + dx, y + dy)
                if e_key_orientation == 'v' and key == ver_char:
                    if move_key in board.bdict and board.bdict[move_key] == key:
                        new_board = self.move_block_piece(board.bdict, key,
                                                          move_key, empty_key1,
                                                          empty_key2)
                        if new_board is not None:
                            new_state = State(new_board, state.depth + 1, state)
                            temp_states.append(new_state)
                elif e_key_orientation == 'h' and key == hor_char:
                    if move_key in board.bdict and board.bdict[move_key] == key:
                        new_board = self.move_block_piece(board.bdict, key,
                                                          move_key, empty_key1,
                                                          empty_key2)
                        if new_board is not None:
                            new_state = State(new_board, state.depth + 1, state)
                            temp_states.append(new_state)
                elif move_key in board.bdict and board.bdict[move_key] == goal_char and move_key[1] + 3 != empty_key2[1]:
                    new_board = self.move_block_piece(board.bdict, key,
                                                      move_key, empty_key1,
                                                      empty_key2)
                    if new_board is not None:
                        new_state = State(new_board, state.depth + 1, state)
                        temp_states.append(new_state)

        return temp_states

    def move_block_piece(self, bdict, pchar, move_key, empty_key1,
                         empty_key2):
        successor_dict = deepcopy(bdict)
        x, y = move_key[0], move_key[1]
        successor_dict.pop(move_key)
        successor_dict.pop(empty_key1)
        successor_dict.pop(empty_key2)
        if pchar == hor_char:
            successor_dict[move_key] = empty_char
            successor_dict[empty_key1] = hor_char
            successor_dict[(x, y + 1)] = empty_char
        elif pchar == ver_char:
            # move right
            successor_dict[move_key] = empty_char
            successor_dict[empty_key1] = ver_char
            successor_dict[(x + 1, y)] = empty_char
        elif pchar == goal_char:
            successor_dict = self.move_goal_piece(bdict, move_key,
                                                  empty_key1, empty_key2)
        new_pieces = self.successor_dict_to_pieces(successor_dict)
        new_board = Board(new_pieces)
        if new_board is not None:
            return new_board

    def move_goal_piece(self, bdict, move_key, empty_key1, empty_key2):
        successor_dict = deepcopy(bdict)
        x, y = move_key[0], move_key[1]

        if y + 2 == empty_key1[1] and (x + 1, y + 2) == empty_key2:
            # move to the right
            successor_dict[(x, y + 1)] = goal_char
            successor_dict[move_key] = empty_char
            successor_dict[(x + 1, y)] = empty_char
        if y - 1 == empty_key1[1] and (x + 1, y - 1) == empty_key2:
            # move to the left
            successor_dict[empty_key1] = goal_char
            successor_dict[(x, y + 1)] = empty_char
            successor_dict[(x + 1, y + 1)] = empty_char
        if x - 1 == empty_key1[0] and (x - 1, y + 1) == empty_key2:
            # move up
            successor_dict[empty_key1] = goal_char
            successor_dict[(x + 1, y)] = empty_char
            successor_dict[(x + 1, y + 1)] = empty_char
        if x + 2 == empty_key1[0] and (x + 2, y + 1) == empty_key2:
            # move down
            successor_dict[(x + 1, y)] = goal_char
            successor_dict[move_key] = empty_char
            successor_dict[(x, y + 1)] = empty_char
        return successor_dict

    @staticmethod
    def successor_dict_to_pieces(dictionary):
        pieces = []
        g_found = False
        for key in dictionary:
            x, y = key[0], key[1]
            char = dictionary[key]
            pieces, g_found = create_pieces_list(char, pieces, g_found, y, x)
        return pieces


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

        for x, ch in enumerate(line.strip()):
            pieces, g_found = create_pieces_list(ch, pieces, g_found, x,
                                                 line_index)
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


def write_output_file(filename, paths):
    puzzle_file = open(filename, "w")
    for path in paths:
        puzzle_file.write(path[0:4])
        puzzle_file.write("\n")
        puzzle_file.write(path[4:8])
        puzzle_file.write("\n")
        puzzle_file.write(path[8:12])
        puzzle_file.write("\n")
        puzzle_file.write(path[12:16])
        puzzle_file.write("\n")
        puzzle_file.write(path[16:20])
        puzzle_file.write("\n")
        puzzle_file.write("\n")


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
    print(args)

    # read the board from the file
    board1 = read_from_file(args.inputfile)
    solver = Solver()
    if args.algo == 'dfs':
        dfs_path, dfs_cost = solver.dfs_solve(board1)
        write_output_file(args.outputfile, dfs_path)
    if args.algo == 'astar':
        a_path, a_cost = solver.a_solve(board1)
        write_output_file(args.outputfile, a_path)




