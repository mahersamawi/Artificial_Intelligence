from Pawn import *
from Board import *


game_board = Board()
game_board.print_board()
moves = game_board.get_valid_moves(game_board.get_pawn(6, 4))
for move in moves:
    print("Move: " + str(move))