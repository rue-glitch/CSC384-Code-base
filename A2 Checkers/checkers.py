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
    def __init__(self, board, depth=None, parent=None, child=None):
        self.board = board
        self.parent = parent
        if depth is None:
            self.depth = 0
        self.depth = depth
        self.child = child

    def display(self):
        for i in self.board.grid:
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
        piece and the value is either the pieces skipped or empty list if it
        takes the spot of an empty piece
        """
        moves = {}
        lcol, rcol = piece[1] - 1, piece[1] + 1
        row = piece[0]
        if player == 'r':
            # need to move upward
            moves.update(
                self.move_left(row - 1, max(row - 3, -1), -1, player, lcol, {}))
            moves.update(
                self.move_right(row - 1, max(row - 3, -1), -1, player, rcol,
                                {}))
        elif player == 'R':
            # need to move upward
            player_lower = player.lower()
            moves.update(
                self.move_left(row - 1, max(row - 3, -1), -1, player_lower,
                               lcol, {}))
            moves.update(
                self.move_right(row - 1, max(row - 3, -1), -1, player_lower,
                                rcol, {}))
            # need to move backward - utilizes the same functionality as b
            # so we'll reuse the b movements
            moves.update(
                self.move_left(row + 1, max(row + 3, 7), 1, player_lower, lcol,
                               {}))
            moves.update(
                self.move_right(row + 1, max(row + 3, 7), 1, player_lower, rcol,
                                {}))
        elif player == 'b':
            # need to move downward
            moves.update(
                self.move_left(row + 1, min(row + 3, 8), 1, player, lcol, {}))
            moves.update(
                self.move_right(row + 1, min(row + 3, 8), 1, player, rcol, {}))
        elif player == 'B':
            # need to move downward
            player_lower = player.lower()
            moves.update(
                self.move_left(row + 1, min(row + 3, 8), 1, player_lower, lcol,
                               {}))
            moves.update(
                self.move_right(row + 1, min(row + 3, 8), 1, player_lower, rcol,
                                {}))
            # need to move upward, same functionality as r
            moves.update(
                self.move_left(row - 1, max(row - 3, -1), -1, player_lower,
                               lcol, {}))
            moves.update(
                self.move_right(row - 1, max(row - 3, -1), -1, player_lower,
                                rcol, {}))
        self.legal_moves.extend(moves)
        return moves

    def move_left(self, start, stop, step, player, lcol, moves, skipped=None):
        if skipped is None:
            skipped = []
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
                    # deleting old key-pair
                    prev_empty_space = (skipped[0][0] - 1, skipped[0][1] - 1)
                    if prev_empty_space in moves:
                        del moves[prev_empty_space]
                    moves[index] = seen + skipped
                    seen = seen + skipped
                    if row == 0:
                        break
                else:
                    # we know it's just an empty piece
                    moves[index] = seen
                if seen:
                    # found something of the other color
                    # need to check number of jumps
                    if step == -1:
                        new_row = max(row - 3, -1)
                    else:
                        new_row = min(row + 3, 7)
                    moves.update(self.move_left(row + step, new_row, step,
                                                player, lcol - 1, moves, seen))
                    moves.update(self.move_right(row + step, new_row, step,
                                                 player, lcol + 1, moves, seen))
                break
            elif index in self.pdict[player] or index in self.pdict[
                player.upper()]:
                # we know it's not a skippable piece
                # need to check if the next piece is empty or not
                break
            elif player == 'r' and (index in self.pdict['b'] or
                                    index in self.pdict['B']):
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            elif player == 'b' and (index in self.pdict['r']
                                    or index in self.pdict['R']):
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            lcol -= 1
        return moves

    def move_right(self, start, stop, step, player, rcol, moves, skipped=None):
        if skipped is None:
            skipped = []
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
                    # deleting old key-pair
                    prev_empty_space = (skipped[0][0] - 1, skipped[0][1] - 1)
                    if prev_empty_space in moves:
                        del moves[prev_empty_space]
                    moves[index] = seen + skipped
                    seen = seen + skipped
                    if row == 7:
                        break
                else:
                    # we know it's any empty piece and we just pass the index
                    # with an empty list as we don't skip over any pieces
                    moves[index] = seen
                if seen:
                    # found something of the other color
                    # need to check number of jumps
                    if step == -1:
                        new_row = max(row - 3, -1)
                    else:
                        new_row = min(row + 3, 8)
                    moves.update(self.move_left(row + step, new_row, step,
                                                player, rcol - 1, moves, seen))
                    moves.update(self.move_right(row + step, new_row, step,
                                                 player, rcol + 1, moves, seen))
                break
            elif index in self.pdict[player] or index in self.pdict[
                player.upper()]:
                # we know it's not a skippable piece
                # need to check if the next piece is empty or not
                break
            elif player == 'r' and (index in self.pdict['b'] or
                                    index in self.pdict['B']):
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            elif player == 'b' and (index in self.pdict['r'] or
                                    index in self.pdict['R']):
                # we know it's a skippable piece
                # need to check if the next piece is empty or not
                seen = [index]
            rcol += 1
        return moves

    def grid_to_str(self):
        string = ''
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                string += str(self.grid[row][col])
        return string


class Game:

    def __init__(self):
        self.seen = set()

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

    def alphabeta(self, state, depth, max_player, alpha, beta):
        if depth == 0 or state.endgame():
            v = self.utility(max_player)
            return v, state

        if max_player:
            if self.cutoff(state, depth):
                return self.eval(state, max_player), state
            max_val = -math.inf
            best_move = None
            children = self.get_children(state, 'r')
            for move in children:
                move.board.turn = 'Black'
                move_str = move.board.grid_to_str()
                if move_str in cache:
                    val = cache[move_str]
                else:
                    val = self.alphabeta(move, depth - 1, False, alpha, beta)[0]
                    cache[move_str] = val
                max_val = max(max_val, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    # prune the remaining children
                    break
                if max_val == val:
                    best_move = move
            return max_val, best_move
        else:
            if self.cutoff(state, depth):
                return self.eval(state, False), state
            min_val = math.inf
            best_move = None
            for move in self.get_children(state, 'b'):
                move.board.turn = 'Red'
                move_str = move.board.grid_to_str()
                if move_str in cache:
                    val = cache[move_str]
                else:
                    val = self.alphabeta(move, depth - 1, True, alpha, beta)[0]
                    cache[move_str] = val
                min_val = min(min_val, val)
                beta = min(beta, val)
                if beta <= alpha:
                    # prune the remaining children
                    break
                if min_val == val:
                    best_move = move
            return min_val, best_move

    def alphabeta_max_node(self, state, max_player, alpha, beta, current_depth, start_time):
        # checking cached state's depth
        # cache[state] = (val, depth, successor_list)
        str_state = state.board.grid_to_str()
        curr_time = time.perf_counter()
        if start_time - curr_time == 110:
            return state
        if str_state in cache and cache[str_state][1] >= current_depth:
            return cache[str_state][0], cache[str_state][2]
        if current_depth == 0:
            return self.eval(state, max_player), None
        successor_list = self.get_children(state, max_player)
        if not successor_list:
            cache[str_state] = (-1000000000, current_depth, None)
            return -1000000000, None
        # sort the successor states based on heuristic_evaluation
        # successors is a list of state objects
        sorted_successors = self.sort_successors(successor_list, max_player)
        v = - math.inf
        best = state
        for successor in sorted_successors:
            tempval, tempstate = self.alphabeta_min_node(successor, False,
                                                         alpha, beta,
                                                         current_depth - 1,
                                                                start_time)
            if tempval > v:
                v = tempval
                best = successor
            if tempval > beta:
                cache[str_state] = (v, current_depth, successor)
                return v, successor
            alpha = max(alpha, tempval)
            cache[str_state] = (v, current_depth, best)
        return v, best

    def alphabeta_min_node(self, state, min_player, alpha, beta, current_depth, start_time):
        # checking cached state's depth
        # cache[state] = (val, depth, successor_list)
        str_state = state.board.grid_to_str()
        curr_time = time.perf_counter()
        if start_time - curr_time == 110:
            return state
        if str_state in cache and cache[str_state][1] >= current_depth:
            return cache[str_state][0], cache[str_state][2]
        if current_depth == 0:
            return self.eval(state, min_player), None
        successor_list = self.get_children(state, min_player)
        if not successor_list:
            cache[str_state] = (1000000000, current_depth, None)
            return 1000000000, None
        # sort the successor states based on heuristic_evaluation
        sorted_successors = self.sort_successors(successor_list, min_player)
        v = math.inf
        best = state
        for successor in sorted_successors:
            tempval, tempstate = self.alphabeta_max_node(successor, True, alpha,
                                                         beta,
                                                         current_depth - 1,
                                                                start_time)
            if tempval < v:
                v = tempval
                best = successor
            if tempval < alpha:
                cache[str_state] = (v, current_depth, successor)
                return v, successor
            beta = min(beta, tempval)
            cache[str_state] = (v, current_depth, best)
        return v, best

    def utility(self, max_player):
        if max_player:
            return + math.inf
        else:
            return - math.inf

    def cutoff(self, state, depth):
        if state.depth == depth:
            return True
        else:
            return False

    def sort_successors(self, successor_list, max_player):
        sorted_dict = {}
        index_list = []
        sorted_successors = []
        for successor in successor_list:
            if successor in cache:
                index = self.eval(successor, max_player)
                if index not in sorted_dict:
                    sorted_dict[index] = [successor]
                    index_list.append(index)
                else:
                    sorted_dict[index].append(successor)
        sorted_indexes = sorted(index_list)
        for index in sorted_indexes:
            sorted_successors.extend(sorted_dict[index])
        return sorted_successors

    def eval(self, state, max_player):
        board = state.board
        if max_player:
            optimization_factor = 0
            for piece_pos in state.board.pdict['R']:
                optimization_factor += self.capturing_potential(piece_pos,
                                                                state.board.pdict,
                                                                max_player)
            return board.red_pieces + board.red_kings * 2 - board.black_pieces \
                   - board.black_kings * 2 + optimization_factor
        else:
            optimization_factor = 0
            for piece_pos in state.board.pdict['B']:
                optimization_factor += self.capturing_potential(piece_pos,
                                                                state.board.pdict,
                                                                max_player)
            return board.black_pieces + board.black_kings * 2 - \
                   board.red_pieces - board.red_kings * 2 + optimization_factor

    def capturing_potential(self, piece_pos, pdict, max_player):
        # we want to optimize for catching pieces
        if max_player:
            row, lcol = piece_pos[0], piece_pos[1]
            if (row - 1, lcol - 1) in pdict['b'] or (row - 1, lcol - 1) in \
                    pdict['B']:
                return 1
            elif (row - 1, lcol + 1) in pdict['b'] or (row - 1, lcol + 1) in \
                    pdict['B']:
                return 1
            elif (row - 1, lcol + 1) in pdict['r'] or (row - 1, lcol + 1) in \
                    pdict['R']:
                return -1
            else:
                return 0
        else:
            row, lcol = piece_pos[0], piece_pos[1]
            if (row + 1, lcol - 1) in pdict['r'] or (row + 1, lcol - 1) in \
                    pdict['R']:
                return 1
            elif (row + 1, lcol + 1) in pdict['r'] or (row + 1, lcol + 1) in \
                    pdict['R']:
                return 1
            elif (row - 1, lcol + 1) in pdict['b'] or (row - 1, lcol + 1) in \
                    pdict['B']:
                return -1
            else:
                return 0

    def get_children(self, state, player):
        parent_board = state.board
        children = []
        if player:
            piece = 'r'
        else:
            piece = 'b'
        moves = self.get_all_moves(parent_board, piece)
        for move in moves:
            piece = move[1]
            old_key = move[0]
            for new_pos in moves[move]:
                new_dict = deepcopy(parent_board.pdict)
                # need to make the key changes
                # new_pos is the key to be added
                if old_key in new_dict[piece]:
                    new_dict[piece].remove(old_key)
                # Kinging the r
                if old_key == 0 and piece == 'r':
                    new_dict['R'].add(new_pos)
                # Kinging the b
                elif move[0] == 7 and piece == 'b':
                    new_dict['B'].add(new_pos)
                else:
                    new_dict[piece].add(new_pos)
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
                # creating the new board's grid
                new_grid = self._dict_to_grid(new_dict)
                # default is red, we update in the parent function
                newBoard = Board(new_grid)
                if newBoard.grid_to_str() not in cache:
                    child = State(newBoard, state.depth + 1, state)
                    state.child = child
                    children.append(child)
        return children

    def get_all_moves(self, board, player):
        """
        Returns all possible moves for the current board state
        """
        moves = {}
        # Implemented node ordering by getting moves for king first as py dict
        # is ordered
        # get moves for the king
        for piece in board.pdict[player.upper()]:
            # get all valid moves for the piece
            possible_moves = board.get_piece_moves(player.upper(), piece)
            moves[(piece, player.upper())] = self.forced_capture(possible_moves)
        # gets moves for each piece
        for piece in board.pdict[player]:
            # get all valid moves for the piece
            possible_moves = board.get_piece_moves(player, piece)
            moves[(piece, player)] = self.forced_capture(possible_moves)
        return moves

    @staticmethod
    def forced_capture(moves):
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

    @staticmethod
    def _dict_to_grid(pdict):
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


def write_to_file(filename, paths):
    puzzle_file = open(filename, "w")
    for path in paths:
        # row 1
        puzzle_file.write(path[0:7])
        puzzle_file.write("\n")
        # row 2
        puzzle_file.write(path[7:14])
        puzzle_file.write("\n")
        # row 3
        puzzle_file.write(path[14:21])
        puzzle_file.write("\n")
        # row 4
        puzzle_file.write(path[21:28])
        puzzle_file.write("\n")
        # row 5
        puzzle_file.write(path[28:35])
        puzzle_file.write("\n")
        # row 6
        puzzle_file.write(path[35:42])
        puzzle_file.write("\n")
        # row 7
        puzzle_file.write(path[42:49])
        puzzle_file.write("\n")
        puzzle_file.write("\n")


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
    state1 = State(initial_board, 0)
    game = Game()
    turn = 'r'
    ctr = 0
    start_time = time.perf_counter()
    result = game.alphabeta_max_node(state1, True, -math.inf, +math.inf, 10, start_time)
    #result = game.alphabeta(state1, 10, True, -math.inf, +math.inf)
    write_to_file(args.outputfile, result.path())

    sys.stdout = open(args.outputfile, 'w')

    sys.stdout = sys.__stdout__

