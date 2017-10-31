from Gamesolver import *

game_board = None
black_pieces = None
white_pieces = None
num_black_wins = 0
num_white_wins = 0
game_running = True
white_nodes_visited = 0
black_nodes_visited = 0

def init_board():
    global game_board
    game_board = Board()
    global black_pieces
    black_pieces = game_board.get_black_pawns()
    global white_pieces
    white_pieces = game_board.get_white_pawns()
    global game_running
    game_running = True

    global white_nodes_visited
    white_nodes_visited = 0

    global black_nodes_visited
    black_nodes_visited = 0

def check_win_conditions():
    if (len(black_pieces) == 0 or len(white_pieces) == 0):
        print("somebody fucked up")
        return False
    for black_pawn in black_pieces:
        pos_x, pos_y = black_pawn.get_position()
        if pos_x == 0:
            global num_black_wins 
            num_black_wins += 1
            print("black wins, visited " + str(black_nodes_visited) + " nodes")
            print("white visited " + str(white_nodes_visited) + " nodes ")
            return False
    for white_pawn in white_pieces:
        pos_x, pos_y = white_pawn.get_position()
        if pos_x == 7:
            global num_white_wins
            num_white_wins += 1
            print("white wins with " + str(white_nodes_visited) + " nodes visited")
            print("black visited " + str(black_nodes_visited) + " nodes ")
            return False
    return True


def move_black(heuristic, depth, is_prune):
    global game_board
    current_pawn, dest, val, nodes_visited = minimax(game_board, depth, heuristic, 'b', is_prune)
    game_board.move_pawn(current_pawn, dest)

    global black_nodes_visited
    black_nodes_visited += nodes_visited


def move_white(heuristic, depth, is_prune):
    global game_board
    current_pawn, dest, val, nodes_visited = minimax(game_board, depth, heuristic, 'w', is_prune)
    game_board.move_pawn(current_pawn, dest)

    global white_nodes_visited
    white_nodes_visited += nodes_visited


# black_pieces = game_board.get_black_pawns()
# for piece in black_pieces:
#     pawn_x, pawn_y = piece.get_position()
#     print("pawn position: (" + str(pawn_x) + ", " + str(pawn_y) + ")")
scenario = 0
black_depth = 4
white_depth = 4

black_prune = True
white_prune = True
init_board()
while (scenario < 10):
    while(game_running):
        # if (scenario % 2 == 0):
        # print("WHITE TURN")
        move_white("defensive2", white_depth, white_prune)
        # game_board.print_board()
        # print("BLACK TURN")
        move_black("offensive1", black_depth, black_prune)
        # game_board.print_board()
        # game_board.scan_board()
        # print("")        
        game_running = check_win_conditions()
    game_board.print_board()
    init_board()
    scenario += 1
    game_running = True
print("Black winrate: " + str((100 * num_black_wins)/scenario))
print("White winrate: " + str((100 * num_white_wins)/scenario))
