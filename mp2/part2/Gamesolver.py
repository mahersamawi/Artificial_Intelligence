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

def offensive_heuristic_2(game_board, color):
    if color == "b":
        black_pawns = game_board.get_black_pawns()
        pawn_distance = []
        for pawn in black_pawns:
            dist = pawn.get_position()[0]
            pawn_distance.append(dist)
        return (1/max(pawn_distance) * 10) + random()
    else:
        white_pawns = game_board.get_white_pawns()
        pawn_distance = []
        for pawn in white_pawns:
            dist = pawn.get_position()[0]
            pawn_distance.append(dist)
        return (max(pawn_distance) * 10) + random()

def defensive_heuristic_2(game_board, color):
    if color == "w":
        black_pawns = game_board.get_black_pawns()
        pawn_distance = []
        for pawn in black_pawns:
            dist = pawn.get_position()[0]
            pawn_distance.append(dist)
        return (1/max(pawn_distance))* 10 + random()
    else:
        white_pawns = game_board.get_white_pawns()
        pawn_distance = []
        for pawn in white_pawns:
            dist = pawn.get_position()[0]
            pawn_distance.append(dist)
        return (max(pawn_distance) * 10) + random()


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
    nodes_visited = 0
    v_list = []
    game_board.update_arrays()
    total_nodes_visited = 0
    if color == "b":
        current_pawns_for_player = game_board.get_black_pawns()
    else:
        current_pawns_for_player = game_board.get_white_pawns()

    for pawn in current_pawns_for_player:
        pawn_x, pawn_y = pawn.get_position()
        for dest_loc in game_board.get_valid_moves(pawn):
            if color == "b":
                if pawn_x == 1:
                    return pawn, dest_loc, float('inf'), total_nodes_visited
            else:
                if pawn_x == 6:
                    return pawn, dest_loc, float('inf'), total_nodes_visited
            dest_loc_pawn = game_board.get_board()[dest_loc[0]][dest_loc[1]]
            prev_pawn = None
            prev_pawn_position = None
            if dest_loc_pawn is not None:
                prev_pawn = dest_loc_pawn
                prev_pawn_position = prev_pawn.get_position()
            # move pawn there
            game_board.move_pawn(pawn, dest_loc)

            nodes_visited += 1
            v, nodes_visited = min_value(game_board, 1, max_depth, color, heuristic, is_prune, alpha, beta)
            total_nodes_visited += nodes_visited
            v_list.append((pawn, dest_loc, v))
            game_board.move_pawn(pawn, (pawn_x, pawn_y))
            if prev_pawn is not None:
                game_board.move_pawn(prev_pawn, prev_pawn_position)
    rt_pawn, rt_dest, rt_value = max(v_list, key=lambda x: x[2])
    return rt_pawn, rt_dest, rt_value, total_nodes_visited


def max_value(game_board, curr_depth, max_depth, parent_color, parent_heuristic, is_prune, alpha, beta):
    if curr_depth == max_depth:
        if parent_heuristic == "offensive1":
            return (offensive_heuristic_1(game_board, parent_color), 0)
        if parent_heuristic == "defensive1":
            return (defensive_heuristic_1(game_board, parent_color), 0)
        if parent_heuristic == "offensive2":
            return (offensive_heuristic_2(game_board, parent_color), 0)
        if parent_heuristic == "defensive2":
            return (defensive_heuristic_2(game_board, parent_color), 0)
    total_nodes_visited = 1
    v = -1 * float('inf')
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
            min_rt_val, nodes_visited = min_value(game_board, curr_depth + 1, max_depth, parent_color, parent_heuristic, is_prune, alpha, beta)
            total_nodes_visited += nodes_visited
            v = max(v, min_rt_val, key=float)
            game_board.move_pawn(pawn, (pawn_x, pawn_y))
            if prev_pawn is not None:
                game_board.move_pawn(prev_pawn, prev_pawn_position)
            if is_prune and (v >= beta):
                #print("Pruning in Max")
                return (v, total_nodes_visited)
            alpha = max(alpha, v)

    return (v, total_nodes_visited)


def min_value(game_board, curr_depth, max_depth, parent_color, parent_heuristic, is_prune, alpha, beta):
    if curr_depth == max_depth:
        if parent_heuristic == "offensive1":
            return (offensive_heuristic_1(game_board, parent_color), 0)
        if parent_heuristic == "defensive1":
            return (defensive_heuristic_1(game_board, parent_color), 0)
        if parent_heuristic == "offensive2":
            return (offensive_heuristic_2(game_board, parent_color), 0)    
        if parent_heuristic == "defensive2":
            return (defensive_heuristic_2(game_board, parent_color), 0)
    total_nodes_visited = 1
    v = float('inf')

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
            max_rt_val, nodes_visited = max_value(game_board, curr_depth + 1, max_depth, parent_color, parent_heuristic, is_prune, alpha, beta)
            v = min(v, max_rt_val, key=float)
            game_board.move_pawn(pawn, (pawn_x, pawn_y))
            if prev_pawn is not None:
                game_board.move_pawn(prev_pawn, prev_pawn_position)
            if is_prune and (v <= alpha):
                # print("Pruning in Min")
                return (v, total_nodes_visited)
            beta = min(beta, v)
    return (v, total_nodes_visited)

