from Gamesolver import *
import time

game_board = None
black_pieces = None
white_pieces = None
num_black_wins = 0
num_white_wins = 0
game_running = True
white_nodes_visited = 0
black_nodes_visited = 0
total_moves = 0
black_moves = 0
white_moves = 0
total_time_for_moves = 0

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

    global total_moves
    total_moves = 0

def check_win_conditions():
    avg_black_nodes_expanded = (black_nodes_visited)/black_moves
    avg_white_nodes_expanded = (white_nodes_visited)/white_moves
    avg_num_nodes_expanded = (white_nodes_visited + black_nodes_visited)/total_moves
    avg_time_per_move = total_time_for_moves/total_moves
    if (len(black_pieces) == 0):
        print("WHITE WINS!!! \nBlack lost all their pieces somehow!!")
        return False
    if (len(white_pieces) == 0):
        print("BLACK WINS!!! \nBlack lost all their pieces somehow!!")
        return False
    for black_pawn in black_pieces:
        pos_x, pos_y = black_pawn.get_position()
        if pos_x == 0:
            global num_black_wins 
            num_black_wins += 1
            game_board.print_board()
            game_board.scan_board()
            print("BLACK WINS!!!")
            print("black visited " + str(black_nodes_visited) + " nodes")
            print("white visited " + str(white_nodes_visited) + " nodes")
            print("White moves: " + str(white_moves))
            print("Black moves: " + str(black_moves))
            print("Total moves: " + str(total_moves))
            print("Average white nodes expanded per move: " + str(avg_white_nodes_expanded))
            print("Average black nodes expanded per move: " + str(avg_black_nodes_expanded))
            print("Average nodes expanded of both types per move: " + str(avg_num_nodes_expanded))
            print("Average time per move: " + str(avg_time_per_move))
            print("Total time elapsed: " + str(total_time_for_moves))
            return False
    for white_pawn in white_pieces:
        pos_x, pos_y = white_pawn.get_position()
        if pos_x == 7:
            global num_white_wins
            num_white_wins += 1
            game_board.print_board()
            game_board.scan_board()
            print("WHITE WINS!!!")
            print("white visited " + str(white_nodes_visited) + " nodes")
            print("black visited " + str(black_nodes_visited) + " nodes")
            print("Total moves: " + str(total_moves))
            print("White moves: " + str(white_moves))
            print("Black moves: " + str(black_moves))
            print("Average white nodes expanded per move: " + str(avg_white_nodes_expanded))
            print("Average black nodes expanded per move: " + str(avg_black_nodes_expanded))
            print("Average nodes expanded of both types per move: " + str(avg_num_nodes_expanded))
            print("Average time per move: " + str(avg_time_per_move))
            print("Total time elapsed: " + str(total_time_for_moves))
            return False
    return True


def move_black(heuristic, depth, is_prune):
    start_time = time.time()
    
    global game_board
    current_pawn, dest, val, nodes_visited = minimax(game_board, depth, heuristic, 'b', is_prune)
    game_board.move_pawn(current_pawn, dest)

    end_time = time.time()
    elapsed_time = end_time - start_time

    global total_time_for_moves
    total_time_for_moves += elapsed_time

    global total_moves
    total_moves += 1

    global black_moves
    black_moves += 1

    global black_nodes_visited
    black_nodes_visited += nodes_visited


def move_white(heuristic, depth, is_prune):
    start_time = time.time()
    global game_board
    current_pawn, dest, val, nodes_visited = minimax(game_board, depth, heuristic, 'w', is_prune)
    game_board.move_pawn(current_pawn, dest)

    end_time = time.time()
    elapsed_time = end_time - start_time

    global total_time_for_moves
    total_time_for_moves += elapsed_time

    global total_moves
    total_moves += 1

    global white_moves
    white_moves += 1

    global white_nodes_visited
    white_nodes_visited += nodes_visited



scenario = 0

white_depth = 4
white_prune = True

black_depth = 4
black_prune = True
init_board()
while (scenario < 1):
    while(game_running):
        move_white("offensive2", white_depth, white_prune)
        move_black("defensive2", black_depth, black_prune)
        game_running = check_win_conditions()
    init_board()
    scenario += 1
    game_running = True
# print("Black winrate: " + str((100 * num_black_wins)/scenario))
# print("White winrate: " + str((100 * num_white_wins)/scenario))
