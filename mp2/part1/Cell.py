
class Cell(object):
    assigned = None
    pos_x = None
    pos_y = None
    color = None
    source = None

    def __init__(self, x, y, color):
        self.pos_x = x
        self.pos_y = y
        if (color == None):
            self.assigned = False
            self.source = False
        else:
            self.assigned = True
            self.source = True
            self.color = color

    def __str__(self):
        if self.color == None:
            return "_"
        return self.color

    def get_assigned(self):
        return self.assigned

    def get_coords(self):
        return self.pos_x, self.pos_y

    def is_source(self):
        return self.source

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def set_assigned(self, assigned):
        self.assigned = assigned

    def get_position(self):
        return self.pos_x, self.pos_y

    def print_position(self):
        print("Cell position: (" + str(self.pos_x) + ", " + str(self.pos_y) + ")" )