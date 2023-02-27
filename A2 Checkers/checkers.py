import argparse
from copy import deepcopy
import math
import sys
import time
from typing import Optional

cache = {}  # you can use this to implement state caching!


class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board, parent=None, child=None):
        self.parent = parent
        self.child = child
        self.board = board
        self.width = 8
        self.height = 8

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")

    def path(self):
        state = self
        path = []
        while state:
            path.append(state.board.grid_to_str())
            state = state.parent
        path.reverse()
        return path

    def endgame(self):
        """
        Checks if the player has run out of moves or pieces
        """
        if self.board.turn == 'Red':
            if (self.board.red_pieces + self.board.red_kings) == 0 and \
                    self.child is None:
                return True
            else:
                return False
        else:
            if (self.board.black_pieces + self.board.black_kings) == 0 and \
                    self.child is None:
                return True
            else:
                return False


class Board:
    """
    Each board is created from the given input.

    Input board:
    ........
    ....b...
    .......R
    ..b.b...
    ...b...r
    ........
    ...r....
    ....B...

    We'll only store the positions of pieces

    pdict: dictionary of set of indexes
    """

    def __init__(self, grid, turn: Optional = None):
        self.grid = grid
        self.pdict = self.grid_to_dict(grid)
        self.red_kings = len(self.pdict['R'])
        self.black_kings = len(self.pdict['B'])
        self.red_pieces = len(self.pdict['r'])
        self.black_pieces = len(self.pdict['b'])
        if turn is None:
            self.turn = 'Red'
        else:
            self.turn = turn
        self.legal_moves = []

    @staticmethod
    def grid_to_dict(grid):
        """
        Converts a grid representation to a dictionary of keys being the players
        or empty spaces and the values being a set of indexes.
        Example:
            pdict = {}
        """
        pdict = {}
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                # adds empty space key to the dict
                if grid[row][col] == '.' and grid[row][col] not in pdict:
                    pdict[grid[row][col]] = {(row, col)}
                # adds index to the empty space key's set
                elif grid[row][col] == '.' and grid[row][col] in pdict:
                    pdict[grid[row][col]].add((row, col))
                # adds pieces' key to the dict
                elif grid[row][col].islower() and grid[row][col] not in pdict:
                    pdict[grid[row][col]] = {(row, col)}
                # adds index to created pieces' set
                elif grid[row][col].islower() and grid[row][col] in pdict:
                    pdict[grid[row][col]].add((row, col))
                # adds king's key to the dict
                elif grid[row][col].isupper() and grid[row][col] not in pdict:
                    pdict[grid[row][col]] = {(row, col)}
                # adds index to created king key's set
                elif grid[row][col].isupper() and grid[row][col] in pdict:
                    pdict[grid[row][col]].add((row, col))
        # if no such piece exists we create it
        if 'R' not in pdict.keys():
            pdict['R'] = {}
        if 'B' not in pdict.keys():
            pdict['B'] = {}
        if 'r' not in pdict.keys():
            pdict['r'] = {}
        if 'b' not in pdict.keys():
            pdict['b'] = {}
        return pdict

    @staticmethod
    def dict_to_grid(pdict):
        """
        Converts a dictionary representation to a grid
        """
        grid = [['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.']]
        for key in pdict:
            for piece in pdict[key]:
                grid[piece[0]][piece[1]] = key
        return grid

    def get_piece_moves(self, player, piece):
        """
        Returns the moves for a specific piece on a board

        Moves is a dictionary where the key is the new position of a particular
        piece and the value is either the pieces skipped or nothing?
        """
        moves = {}
        lcol, rcol = piece[1] - 1, piece[1] + 1
        row = piece[0]
        # works if given correct player but incorrect index -> TODO: check if
        # this is a problem in game play
        # need to figure out how to remove players who become kings
        if player == 'r':
            # need to move upward
            moves.update(self.move_left(row -1, max(row -3, -1), -1, player, lcol))
            moves.update(self.move_right(row -1, max(row -3, -1), -1, player, rcol))
        elif player == 'R':
            # need to move upward
            moves.update(self.move_left(row -1, max(row -3, -1), -1, player, lcol))
            moves.update(self.move_right(row -1, max(row -3, -1), -1, player, rcol))
            # need to move backward - utilizes the same functionality as b
            # so we'll reuse the b movements
            moves.update(self.move_left(row + 1, max(row + 3, 7), 1, player, lcol))
            moves.update(self.move_right(row + 1, max(row + 3, 7), 1, player, rcol))
        elif player == 'b':
            # need to move downward
            moves.update(self.move_left(row + 1, min(row + 3, 7), 1, player, lcol))
            moves.update(self.move_right(row + 1, min(row + 3, 7), 1, player, rcol))
        elif player == 'B':
            # need to move downward
            moves.update(self.move_left(row + 1, min(row + 3, 7), 1, player, lcol))
            moves.update(self.move_right(row + 1, min(row + 3, 7), 1, player, rcol))
            # need to move upward, same functionality as r
            moves.update(self.move_left(row -1, max(row -3, -1), -1, player, lcol))
            moves.update(self.move_right(row -1, max(row -3, -1), -1, player, rcol))
        self.legal_moves.extend(moves)
        return moves

    def move_left(self, start, stop, step, color, lcol, skipped=[]):
        moves = {}
        seen = []
        for row in range(start, stop, step):
            # check if current piece is an empty piece
            index = (row, lcol)

            if lcol < 0:
                break

            if index in self.pdict['.']:
                if skipped and not seen:
                    break
                elif skipped:
                    # need to figure out the king situation
                    moves[index] = seen + skipped
                    seen = seen + skipped
                    if row == 0:
                        break
                else:
                    # we know it's any empty piece and we just pass the index with
                    # an empty list as we don't skip over any pieces
                    moves[index] = seen
                if seen:
                    # found something of the other color
                    # need to check number of jumps
                    if step == -1:
                        new_row = max(row-3, -1)
                    else:
                        new_row = min(row+3, 7)
                    moves.update(self.move_left(row + step, new_row, step, color, lcol -1, skipped=seen))
                    moves.update(self.move_right(row + step, new_row, step, color, lcol + 1, skipped=seen))
                break
            elif index in self.pdict[color]:
                # we know it's not a skippable piece
                # need to check if the next piece is empty or not
                break
            elif color == 'r' or color == 'R' and index in self.pdict['b']:
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            elif color == 'b' or color == 'B' and index in self.pdict['r']:
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            elif color == 'r' or color == 'R' and index in self.pdict['B']:
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            elif color == 'b' or color == 'B' and index in self.pdict['R']:
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            lcol -= 1
        return moves

    def move_right(self, start, stop, step, color, rcol, skipped=[]):
        moves = {}
        seen = []
        for row in range(start, stop, step):
            index = (row, rcol)
            if rcol > 7:
                break
            # check if current piece is an empty piece
            if index in self.pdict['.']:
                if skipped and not seen:
                    break
                elif skipped:
                    moves[index] = seen + skipped
                    seen = seen + skipped
                    if row == 7:
                        break
                else:
                    # we know it's any empty piece and we just pass the index with
                    # an empty list as we don't skip over any pieces
                    moves[index] = seen
                if seen:
                    # found something of the other color
                    # need to check number of jumps
                    if step == -1:
                        new_row = max(row-3, -1)
                    else:
                        new_row = min(row+3, 8)
                    moves.update(self.move_left(row + step, new_row, step, color, rcol -1, skipped=seen))
                    moves.update(self.move_right(row + step, new_row, step, color, rcol + 1, skipped=seen))
                break
            elif index in self.pdict[color]:
                # we know it's not a skippable piece
                # need to check if the next piece is empty or not
                break
            elif color == 'r' or color == 'R' and index in self.pdict['b']:
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            elif color == 'b' or color == 'B' and index in self.pdict['r']:
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            elif color == 'r' or color == 'R' and index in self.pdict['B']:
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            elif color == 'b' or color == 'B' and index in self.pdict['R']:
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            rcol += 1
        return moves

    def utility(self):
        if self.turn == 'Red':
            return self.red_pieces + self.red_kings*2 - self.black_pieces + self.black_kings*2
        elif self.turn == 'Black':
            return self.black_pieces + self.black_kings*2 - self.red_pieces - self.red_kings*2

    def grid_to_str(self):
        string = ''
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                string += str(self.grid[row][col])
        return string


class Game:

    def __init__(self):
        self.seen = set()

    def minimax(self, depth, state, max_player):
        # At the last state in the tree or won the game
        if depth == 0 or state.endgame():
            return state.board.utility(), state.board

        if max_player:
            max_val = -math.inf
            best_move = None
            for move in self.get_children(state, 'r'):
                move.board.turn = 'Black'
                value = self.minimax(depth - 1, move, False)[0]
                max_val = max(max_val, value)
                if max_val == value:
                    best_move = move.board
            return max_val, best_move
        else:
            min_val = math.inf
            best_move = None
            for move in self.get_children(state, 'b'):
                move.board.turn = 'Red'
                value = self.minimax(depth - 1, move, True)[0]
                min_val = min(min_val, value)
                if min_val == value:
                    best_move = move.board
            return min_val, best_move

    """
    def alphabeta(self, depth, board, max_player, alpha, beta):
        # At the last state in the tree or won the game
        if depth == 0 or board.endgame():
            return board.utility(), board

        if max_player:
            alpha = -math.inf
            best_move = None
            for move in self.get_children(board, 'r'):
                value = self.alphabeta(depth-1, move, False, alpha, beta)
                max_val = max(max_val, value[0])
                if max_val == value[0]:
                    best_move = value[1]
            return max_val, best_move
        else:
            min_val = math.inf
            best_move = None
            for move in self.get_children(board, 'b'):
                value = self.alphabeta(depth-1, move, True, alpha, beta)
                min_val = min(min_val, value[0])
                if min_val == value[0]:
                    best_move = value[1]
            return min_val, best_move
    """

    def alphabeta(self, depth, state, max_player, alpha, beta):
        if depth == 0 or state.endgame():
            val = state.board.utility()
            return state.board.utility(), state.board

        if max_player:
            max_val = -math.inf
            best_move = None
            for move in self.get_children(state, 'r'):
                move.board.turn = 'Black'
                value = self.alphabeta(depth-1, move, False, alpha, beta)[0]
                max_val = max(max_val, value)
                alpha = max(max_val, alpha)
                if beta <= alpha:
                    break
                if max_val == value:
                    best_move = move.board
            return max_val, best_move
        else:
            min_val = math.inf
            best_move = None
            for move in self.get_children(state, 'b'):
                move.board.turn = 'Red'
                value = self.alphabeta(depth-1, move, True, alpha, beta)[0]
                min_val = min(min_val, value)
                beta = min(min_val, beta)
                if beta <= alpha:
                    break
                if min_val == value:
                    best_move = move.board
            return min_val, best_move

    def get_children(self, state, player):
        parent_board = state.board
        children = []
        moves = self.get_all_moves(parent_board, player)
        for move in moves:
            for new_pos in moves[move]:
                new_dict = deepcopy(parent_board.pdict)
                # need to make the key changes
                # move is the new key and values is the keys to remove
                if move[0] in new_dict[move[1]]:
                    new_dict[move[1]].remove(move[0])
                if move[0] == 0 and player == 'r':
                    player = 'R'
                    new_dict['r'].remove(move)
                if move[0] == 7 and player == 'b':
                    player = 'B'
                    new_dict['b'].remove(move)
                new_dict[move[1]].add(new_pos)
                for val in moves[move][new_pos]:
                    # removes the captured values
                    if val in new_dict['b']:
                        new_dict['b'].remove(val)
                    elif val in new_dict['B']:
                        new_dict['B'].remove(val)
                    elif val in new_dict['r']:
                        new_dict['r'].remove(val)
                    elif val in new_dict['R']:
                        new_dict['R'].remove(val)
                newBoard = Board(grid=parent_board.grid)
                newBoard.pdict = new_dict
                newBoard.grid = newBoard.dict_to_grid(new_dict)
                child = State(newBoard, state)
                children.append(child)
        return children

    def get_all_moves(self, board, player):
        """
        Returns all possible moves for the current board state
        """
        moves = {}
        # gets moves for each piece
        for piece in board.pdict[player]:
            # get all valid moves for the piece
            possible_moves = board.get_piece_moves(player, piece)
            moves[(piece, player)] = self.forced_capture(possible_moves)
        # get moves for the king too
        for piece in board.pdict[player.upper()]:
            # get all valid moves for the piece
            moves[(piece, player.upper())] = board.get_piece_moves(player, piece)
        return moves

    def forced_capture(self, moves):
        capture = False
        capturing_moves = {}
        for move in moves:
            if len(moves[move]) > 0:
                capture = True
                capturing_moves[move] = moves[move]
        if capture:
            return capturing_moves
        else:
            return moves


def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']


def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'


def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    state = State(initial_board)
    turn = 'r'
    ctr = 0

    sys.stdout = open(args.outputfile, 'w')

    sys.stdout = sys.__stdout__
