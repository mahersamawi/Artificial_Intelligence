from Pawn import *
from Board import *
from random import *

def defensive_heuristic_1(game_board, color):
    num_pawns_rem = game_board.get_number_of_pawns(color)
    return 2 * num_pawns_rem + random()


def offensive_heuristic_1(game_board, color):
    if color == "w":
        black_pawns_rem = game_board.get_number_of_pawns("b")
        return 2 * (30 - black_pawns_rem) + random()
    else:
        white_pawns_rem = game_board.get_number_of_pawns("w")
        return 2 * (30 - white_pawns_rem) + random()

"""
Alpha beta pruning
"""




def print_potential_moves(v_list):
    for thing in v_list:
        pawn_x, pawn_y = thing[0].get_position()
        dest_loc = thing[1]
        print("pawn location: (" + str(pawn_x) + ", " + str(pawn_y) + ")")
        print("pawn destination: (" + str(dest_loc[0]) + ", " + str(dest_loc[1]) + ")")


def minimax(game_board, max_depth, heuristic, color, is_prune):
    infinity = float('inf')
    alpha = -infinity
    beta = infinity

    v_list = []
    game_board.update_arrays()
    if color == "b":
        current_pawns_for_player = game_board.get_black_pawns()
    else:
        current_pawns_for_player = game_board.get_white_pawns()

    for pawn in current_pawns_for_player:
        pawn_x, pawn_y = pawn.get_position()
        for dest_loc in game_board.get_valid_moves(pawn):
            if color == "b":
                if pawn_x == 1:
                    return pawn, dest_loc, float('inf')
            else:
                if pawn_x == 6:
                    return pawn, dest_loc, float('inf')
            dest_loc_pawn = game_board.get_board()[dest_loc[0]][dest_loc[1]]
            prev_pawn = None
            prev_pawn_position = None
            if dest_loc_pawn is not None:
                prev_pawn = dest_loc_pawn
                prev_pawn_position = prev_pawn.get_position()
            # move pawn there
            game_board.move_pawn(pawn, dest_loc)

            v = min_value(game_board, 1, max_depth, color, heuristic, is_prune, alpha, beta)
            v_list.append((pawn, dest_loc, v))
            game_board.move_pawn(pawn, (pawn_x, pawn_y))
            if prev_pawn is not None:
                game_board.move_pawn(prev_pawn, prev_pawn_position)
    return max(v_list, key=lambda x: x[2])


def max_value(game_board, curr_depth, max_depth, parent_color, parent_heuristic, is_prune, alpha, beta):
    if curr_depth == max_depth:
        if parent_heuristic == "offensive":
            return offensive_heuristic_1(game_board, parent_color)
        if parent_heuristic == "defensive":
            return defensive_heuristic_1(game_board, parent_color)
    
    infinity = float('inf')
    v = -infinity
    if parent_color == "b":
        current_pieces_max = game_board.get_black_pawns()
    else:
        current_pieces_max = game_board.get_white_pawns()
    for pawn in current_pieces_max:
        pawn_x, pawn_y = pawn.get_position()
        for dest_loc in game_board.get_valid_moves(pawn):
            dest_loc_pawn = game_board.get_board()[dest_loc[0]][dest_loc[1]]
            prev_pawn = None
            if dest_loc_pawn is not None:
                prev_pawn = dest_loc_pawn
                prev_pawn_position = prev_pawn.get_position()
            # move pawn there
            game_board.move_pawn(pawn, dest_loc)
            # recurse
            v = max(v, min_value(game_board, curr_depth + 1, max_depth, parent_color, parent_heuristic, is_prune, alpha, beta), key=float)
            game_board.move_pawn(pawn, (pawn_x, pawn_y))
            if prev_pawn is not None:
                game_board.move_pawn(prev_pawn, prev_pawn_position)
            if is_prune and (v >= beta):
                #print("Pruning in Max")
                return v
            alpha = max(alpha, v)

    return v


def min_value(game_board, curr_depth, max_depth, parent_color, parent_heuristic, is_prune, alpha, beta):
    if curr_depth == max_depth:
        if parent_heuristic == "offensive":
            return offensive_heuristic_1(game_board, parent_color)
        if parent_heuristic == "defensive":
            return defensive_heuristic_1(game_board, parent_color)

    infinity = float('inf')
    v = infinity

    if parent_color == "b":
        current_pieces_min = game_board.get_white_pawns()
    else:
        current_pieces_min = game_board.get_black_pawns()
    for pawn in current_pieces_min:
        pawn_x, pawn_y = pawn.get_position()
        for dest_loc in game_board.get_valid_moves(pawn):
            dest_loc_pawn = game_board.get_board()[dest_loc[0]][dest_loc[1]]
            prev_pawn = None
            prev_pawn_position = None
            if dest_loc_pawn is not None:
                prev_pawn = dest_loc_pawn
                prev_pawn_position = prev_pawn.get_position()
            # move pawn there
            game_board.move_pawn(pawn, dest_loc)
            # recurse
            v = min(v, max_value(game_board, curr_depth + 1, max_depth, parent_color, parent_heuristic, is_prune, alpha, beta), key=float)
            game_board.move_pawn(pawn, (pawn_x, pawn_y))
            if prev_pawn is not None:
                game_board.move_pawn(prev_pawn, prev_pawn_position)
            if is_prune and (v <= alpha):
                # print("Pruning in Min")
                return v
            beta = min(beta, v)
    return v

