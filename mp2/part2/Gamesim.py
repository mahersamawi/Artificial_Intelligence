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
        print("somebody fucked up")
        return False
    for black_pawn in black_pieces:
        pos_x, pos_y = black_pawn.get_position()
        if pos_x == 0:
            print("black wins")
            return False
    for white_pawn in white_pieces:
        pos_x, pos_y = white_pawn.get_position()
        if pos_x == 7:
            print("white wins")
            return False
    return True

def move_black(heuristic):
    current_pawn, dest, val = minimax_black(game_board, 3, heuristic)
    game_board.move_pawn(current_pawn, dest)

def move_white(heuristic):
    current_pawn, dest, val = minimax_white(game_board, 3, heuristic)
    game_board.move_pawn(current_pawn, dest)

game_running = True

# black_pieces = game_board.get_black_pawns()
# for piece in black_pieces:
#     pawn_x, pawn_y = piece.get_position()
#     print("pawn position: (" + str(pawn_x) + ", " + str(pawn_y) + ")")
while(game_running):
    print("WHITE TURN")
    move_white("offensive")
    game_board.print_board()
    print("\n")
    print("BLACK TURN")
    move_black("defensive")
    game_board.print_board()

    game_board.scan_board()
    game_running = check_win_conditions()
    print("\n")
