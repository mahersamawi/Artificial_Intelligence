from Pawn import *
from Board import *
import random

game_board = Board()
game_board.print_board()
test_pawn = game_board.get_pawn(6, 4)
moves = game_board.get_valid_moves(test_pawn)
for move in moves:
    print("Move: " + str(move))
game_board.move_pawn(test_pawn, moves[2])
game_board.print_board()

def defensive_heuristic_1(color):
    num_pawns_rem = game_board.get_number_of_pawns(color)
    return 2 * num_pawns_rem + random()

def offensive_heuristic_1(color):
    if color == "w":
        black_pawns_rem = game_board.get_number_of_pawns("b")
        return 2 * (30 - black_pawns_rem) + random()
    else:
        white_pawns_rem = game_board.get_number_of_pawns("w")
        return 2 * (30 - white_pawns_rem) + random()