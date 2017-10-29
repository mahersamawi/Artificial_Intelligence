from Gamesolver import *

game_board = Board()
black_pieces = game_board.get_black_pawns()
white_pieces = game_board.get_white_pawns()
# test_pawn = game_board.get_pawn(6, 4)
# moves = game_board.get_valid_moves(test_pawn)
# for move in moves:
#     print("Move: " + str(move))
# game_board.move_pawn(test_pawn, (1,1))
# game_board.print_board()
# print(minimax())


def check_win_conditions():
    if (len(black_pieces) == 0 or len(black_pieces) == 0):
        return False
    for black_pawn in black_pieces:
        pos_x, pos_y = black_pawn.get_position()
        if pos_x == 0:
            return False
    for white_pawn in white_pieces:
        pos_x, pos_y = white_pawn.get_position()
        if pos_x == 7:
            return False
    return True
game_running = True
i = 0
# black_pieces = game_board.get_black_pawns()
# for piece in black_pieces:
#     pawn_x, pawn_y = piece.get_position()
#     print("pawn position: (" + str(pawn_x) + ", " + str(pawn_y) + ")")
while(game_running):
    current_pawn, dest, val = minimax_black(game_board, 2, "offensive")
    game_board.move_pawn(current_pawn, dest)
    game_board.print_board()
    game_running = check_win_conditions()
    game_board.scan_board()
    print("\n")
    i += 1


print("\n")
game_board.print_board()