class Pawn(object):
    pos_x = None
    pos_y = None
    color = None

    def __init__(self, x, y, color):
        self.pos_x = x
        self.pos_y = y
        self.color = color

    def get_position(self):
        return self.pos_x, self.pos_y

    def get_color(self):
        return self.color

    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def print_pawn(self):
        print(self.color, end="")

    def get_position_str(self):
        return "(" + str(self.pos_x) + ", " + str(self.pos_y) + ")"