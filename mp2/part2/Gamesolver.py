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

def print_potential_moves(v_list):
    for thing in v_list:
        pawn_x, pawn_y = thing[0].get_position()
        dest_loc = thing[1]
        print("pawn location: (" + str(pawn_x) + ", " + str(pawn_y) + ")")
        print("pawn destination: (" + str(dest_loc[0]) + ", " + str(dest_loc[1]) + ")")

def minimax_black(game_board, max_depth, heuristic):
    v_list = []
    for pawn in game_board.get_black_pawns():
        pawn_x, pawn_y = pawn.get_position()
        # print("pawn location: (" + str(pawn_x) + ", " + str(pawn_y) + ")")
        for dest_loc in game_board.get_valid_moves(pawn):
            # print("pawn destination: (" + str(dest_loc[0]) + ", " + str(dest_loc[1]) + ")")
            if (pawn_x == 1):
                return (pawn, dest_loc, float('inf'))
            dest_loc_pawn = game_board.get_board()[dest_loc[0]][dest_loc[1]]
            prev_pawn = None
            prev_pawn_position = None
            if dest_loc_pawn is not None:
                prev_pawn = dest_loc_pawn
                prev_pawn_position = prev_pawn.get_position()
            # move pawn there
            # game_board.move_pawn(None, pawn.get_position())
            game_board.move_pawn(pawn, dest_loc)

            v = min_value(game_board, 1, max_depth, "b", heuristic)
            # print("v in minimax is " + str(v))
            v_list.append((pawn, dest_loc, v))
            game_board.move_pawn(pawn, (pawn_x, pawn_y))
            if prev_pawn is not None:
                # print("putting pawn of color " + prev_pawn.get_color() + " back in min_Value at " + prev_pawn.get_position_str())
                game_board.move_pawn(prev_pawn, prev_pawn_position)
    # print_potential_moves(v_list)
    return max(v_list, key=lambda x: x[2])

def minimax_white(game_board, max_depth, heuristic):
    v_list = []
    for pawn in game_board.get_white_pawns():
        pawn_x, pawn_y = pawn.get_position()
        for dest_loc in game_board.get_valid_moves(pawn):
            if (pawn_x == 6):
                return (pawn, dest_loc, -1 * float('inf'))
            dest_loc_pawn = game_board.get_board()[dest_loc[0]][dest_loc[1]]
            prev_pawn = None
            if dest_loc_pawn is not None:
                prev_pawn = dest_loc_pawn
                prev_pawn_position = prev_pawn.get_position()
            # move pawn there
            game_board.move_pawn(pawn, dest_loc)
            v = max_value(game_board, 1, max_depth, "w", heuristic)
            # print("v in minimax is " + str(v))
            v_list.append((pawn, dest_loc, v))
            game_board.move_pawn(pawn, (pawn_x, pawn_y))
            if prev_pawn is not None:
                game_board.move_pawn(prev_pawn, prev_pawn_position)
    # print_potential_moves(v_list)
    return max(v_list, key=lambda x: x[2])

def max_value(game_board, curr_depth, max_depth, parent_color, parent_heuristic):
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
                # print("Dest pawn is not none")
                prev_pawn = dest_loc_pawn
                prev_pawn_position = prev_pawn.get_position()
            # move pawn there
            game_board.move_pawn(pawn, dest_loc)
            # recurse
            v = max(v, min_value(game_board, curr_depth + 1, max_depth, parent_color, parent_heuristic), key=float)
            game_board.move_pawn(pawn, (pawn_x, pawn_y))
            if prev_pawn is not None:
                # print("putting pawn back at " + prev_pawn.get_position_str())
                game_board.move_pawn(prev_pawn, prev_pawn_position)

    # print("max is " + str(v))
    return v


def min_value(game_board, curr_depth, max_depth, parent_color, parent_heuristic):
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
            v = min(v, max_value(game_board, curr_depth + 1, max_depth, parent_color, parent_heuristic), key=float)
            game_board.move_pawn(pawn, (pawn_x, pawn_y))
            if prev_pawn is not None:
                # print("putting pawn of color " + prev_pawn.get_color() + " back in min_Value at " + prev_pawn.get_position_str())
                game_board.move_pawn(prev_pawn, prev_pawn_position)
    # print("min is " + str(v))
    return v

