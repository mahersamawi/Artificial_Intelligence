from Pawn import *
from Board import *
from random import *


def defensive_heuristic_1(color):
    num_pawns_rem = game_board.get_number_of_pawns(color)
    return 2 * num_pawns_rem


def offensive_heuristic_1(color):
    if color == "w":
        black_pawns_rem = game_board.get_number_of_pawns("b")
        return 2 * (30 - black_pawns_rem) + random()
    else:
        white_pawns_rem = game_board.get_number_of_pawns("w")
        return 2 * (30 - white_pawns_rem) + random()


def minimax():
    v_list = []
    count = 0
    for pawn in game_board.get_black_pawns():
        for dest_loc in game_board.get_valid_moves(pawn):
            dest_loc_pawn = game_board.get_board()[dest_loc[0]][dest_loc[1]]
            prev_pawn = None
            if dest_loc_pawn is not None:
                prev_pawn = dest_loc_pawn
            # move pawn there
            game_board.move_pawn(pawn, dest_loc)
            v = min_value(1, 3)
            print("v in minimax is " + str(v))
            v_list.append((pawn, dest_loc, v))
            if prev_pawn is not None:
                game_board.move_pawn(prev_pawn, prev_pawn.get_position())

    return max(v_list, key=lambda x: x[2])


def max_value(curr_depth, max_depth):
    if curr_depth == max_depth:
        return offensive_heuristic_1("w")
    v = 0.0
    for pawn in game_board.get_black_pawns():
        for dest_loc in game_board.get_valid_moves(pawn):
            dest_loc_pawn = game_board.get_board()[dest_loc[0]][dest_loc[1]]
            prev_pawn = None
            if dest_loc_pawn is not None:
                prev_pawn = dest_loc_pawn
            # move pawn there
            game_board.move_pawn(pawn, dest_loc)
            # recurse
            v = max(v, min_value(curr_depth + 1, max_depth), key=float)
            if prev_pawn is not None:
                game_board.move_pawn(prev_pawn, prev_pawn.get_position())

    print("max is " + str(v))
    return v


def min_value(curr_depth, max_depth):
    if curr_depth == max_depth:
        return offensive_heuristic_1("w")

    v = 1000.0

    for pawn in game_board.get_white_pawns():
        for dest_loc in game_board.get_valid_moves(pawn):
            dest_loc_pawn = game_board.get_board()[dest_loc[0]][dest_loc[1]]
            prev_pawn = None
            if dest_loc_pawn is not None:
                prev_pawn = dest_loc_pawn
            # move pawn there
            game_board.move_pawn(pawn, dest_loc)
            # recurse
            v = min(v, max_value(curr_depth + 1, max_depth), key=float)
            if prev_pawn is not None:
                game_board.move_pawn(prev_pawn, prev_pawn.get_position())
    print("min is " + str(v))
    return v


game_board = Board()
game_board.print_board()
test_pawn = game_board.get_pawn(6, 4)
moves = game_board.get_valid_moves(test_pawn)
for move in moves:
    print("Move: " + str(move))
game_board.move_pawn(test_pawn, (1,1))
game_board.print_board()
print(minimax())
