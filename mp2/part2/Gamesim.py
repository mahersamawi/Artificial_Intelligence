from Gamesolver import *

game_board = None
black_pieces = None
white_pieces = None
num_black_wins = 0
num_white_wins = 0
game_running = True


def init_board():
    global game_board
    game_board = Board()
    global black_pieces
    black_pieces = game_board.get_black_pawns()
    global white_pieces
    white_pieces = game_board.get_white_pawns()
    global game_running
    game_running = True

def check_win_conditions():
    if (len(black_pieces) == 0 or len(white_pieces) == 0):
        print("somebody fucked up")
        return False
    for black_pawn in black_pieces:
        pos_x, pos_y = black_pawn.get_position()
        if pos_x == 0:
            global num_black_wins 
            num_black_wins += 1
            print("black wins")
            return False
    for white_pawn in white_pieces:
        pos_x, pos_y = white_pawn.get_position()
        if pos_x == 7:
            global num_white_wins
            num_white_wins += 1
            print("white wins")
            return False
    return True


def move_black(heuristic, depth):
    global game_board
    current_pawn, dest, val = minimax(game_board, 4, heuristic, 'b', True)
    game_board.move_pawn(current_pawn, dest)


def move_white(heuristic, depth):
    global game_board
    current_pawn, dest, val = minimax(game_board, 3, heuristic, 'w', False)
    game_board.move_pawn(current_pawn, dest)


# black_pieces = game_board.get_black_pawns()
# for piece in black_pieces:
#     pawn_x, pawn_y = piece.get_position()
#     print("pawn position: (" + str(pawn_x) + ", " + str(pawn_y) + ")")
scenario = 0
init_board()
while (scenario < 1):
    while(game_running):
        if (scenario % 2 == 0):
            move_black("offensive", 3)
            move_white("offensive", 3)
        else:
            move_white("offensive", 3)
            move_black("offensive", 3)
        # print("WHITE TURN")
        # game_board.print_board()
        # print("\n")
        # print("BLACK TURN")
        
        game_board.print_board()
        # game_board.scan_board()
        game_running = check_win_conditions()
        # print("\n")
    #game_board.print_board()
    init_board()
    scenario += 1
    game_running = True
print("Black winrate: " + str((100 * num_black_wins)/scenario))
print("White winrate: " + str((100 * num_white_wins)/scenario))
