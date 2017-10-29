from Gamesolver import *

game_board = Board()
black_pieces = game_board.get_black_pawns()
white_pieces = game_board.get_white_pawns()
num_black_wins = 0
num_white_wins = 0

def check_win_conditions(b_pieces, w_pieces):
    if (len(b_pieces) == 0 or len(w_pieces) == 0):
        print("somebody fucked up")
        return False
    for black_pawn in b_pieces:
        pos_x, pos_y = black_pawn.get_position()
        if pos_x == 0:
            global num_black_wins 
            num_black_wins += 1
            print("black wins")
            return False
    for white_pawn in w_pieces:
        pos_x, pos_y = white_pawn.get_position()
        if pos_x == 7:
            global num_white_wins
            num_white_wins += 1
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
scenario = 0
while (scenario < 10):
    while(game_running):
        # print("WHITE TURN")
        move_white("offensive")
        # game_board.print_board()
        # print("\n")
        # print("BLACK TURN")
        move_black("defensive")
        # game_board.print_board()
        # game_board.scan_board()
        game_running = check_win_conditions(black_pieces, white_pieces)
        # print("\n")
    game_board.print_board()
    game_board = Board()
    black_pieces = game_board.get_black_pawns()
    white_pieces = game_board.get_white_pawns()    
    scenario += 1
    game_running = True
print("Black winrate: " + str((100 * num_black_wins)/scenario))
print("White winrate: " + str((100 * num_white_wins)/scenario))
