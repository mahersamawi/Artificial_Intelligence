from Pawn import *


class Board(object):
    board_array = None
    white_pawns = []
    black_pawns = []

    def __init__(self):
        self.board_array = [[None for x in range(8)] for y in range(8)]

        for i in range(2):
            for j in range(8):
                white_pawn = Pawn(i, j, "w")
                self.board_array[i][j] = white_pawn
                self.white_pawns.append(white_pawn)
        for i in range(6, 8):
            for j in range(8):
                black_pawn = Pawn(i, j, "b")
                self.board_array[i][j] = black_pawn
                self.black_pawns.append(black_pawn)

    def get_pawn(self, x, y):
        if x > 7 or y > 7 or x < 0 or y < 0:
            return "invalid"
        return self.board_array[x][y]

    def get_board(self):
        return self.board_array

    def print_board(self):
        for i in range(8):
            for j in range(8):
                pawn = self.board_array[i][j]
                if pawn != None:
                    pawn.print_pawn()
                    print("|", end="")
                else:
                    print("-", end="|")
            print("")
    def scan_board(self):
        num_black_pawns = 0
        num_white_pawns = 0
        for i in range(8):
            for j in range(8):
                pawn = self.board_array[i][j]
                if pawn != None:
                    # print("pawn position: " + pawn.get_position_str() )
                    if pawn.get_color() == "w":
                        num_white_pawns += 1    
                    else:
                        num_black_pawns += 1    
        print("Num black pawns: " + str(num_black_pawns))
        print("Num white pawns: " + str(num_white_pawns))


    def update_arrays(self):
        self.white_pawns = []
        self.black_pawns = []
        for i in range(8):
            for j in range(8):
                pawn = self.board_array[i][j]
                if pawn != None:
                    # print("pawn position: " + pawn.get_position_str() )
                    if pawn.get_color() == "w":
                        self.white_pawns.append(pawn)
                    else:
                        self.black_pawns.append(pawn)
    def get_number_of_pawns(self, color):
        if color == "w":
            return len(self.white_pawns)
        else:
            return len(self.black_pawns)

    def move_pawn(self, pawn, dest_tuple):
        pawn_pos = pawn.get_position()
        self.board_array[pawn_pos[0]][pawn_pos[1]] = None
        self.board_array[dest_tuple[0]][dest_tuple[1]] = pawn
        pawn.set_position(dest_tuple[0], dest_tuple[1])

    def set_pawn(self, pawn, dest_tuple):
        self.board_array[dest_tuple[0]][dest_tuple[1]] = pawn
        if (pawn != None):
            pawn.set_position(dest_tuple[0], dest_tuple[1])
    
    def get_white_pawns(self):
        return self.white_pawns

    def get_black_pawns(self):
        return self.black_pawns

    # moves are strings: up, upleft, upright, down, downleft, downright
    def get_valid_moves(self, pawn):
        game_board = self
        valid_moves = []
        pawn_color = pawn.get_color()
        pawn_x, pawn_y = pawn.get_position()
        if (pawn_color == "w"):
            # check downleft
            temp = game_board.get_pawn(pawn_x+1, pawn_y-1)
            if (temp == None) or ((temp != "invalid") and (temp.get_color() == "b")):
                valid_moves.append((pawn_x+1, pawn_y-1))

            # check down
            temp = game_board.get_pawn(pawn_x+1, pawn_y)
            if (temp == None):
                valid_moves.append((pawn_x+1, pawn_y))

            # check downright
            temp = game_board.get_pawn(pawn_x+1, pawn_y+1)
            if (temp == None) or ((temp != "invalid") and (temp.get_color() == "b")):
                valid_moves.append((pawn_x+1, pawn_y+1))

            

        if (pawn_color == "b"):
            # check upleft
            temp = game_board.get_pawn(pawn_x-1, pawn_y-1)
            if (temp == None) or ((temp != "invalid") and (temp.get_color() == "w")):
                valid_moves.append((pawn_x-1, pawn_y-1))

            # check up
            temp = game_board.get_pawn(pawn_x-1, pawn_y)
            if (temp == None):
                valid_moves.append((pawn_x-1, pawn_y))

            # check upright
            temp = game_board.get_pawn(pawn_x-1, pawn_y+1)
            if (temp == None) or ((temp != "invalid") and (temp.get_color() == "w")):
                valid_moves.append((pawn_x-1, pawn_y+1))

            

        return valid_moves
