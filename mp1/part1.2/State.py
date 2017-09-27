class State(object):

    number_of_dots_left = None
    position = None

    def __init__(self, pos, dot_len):
        self.position = pos
        self.number_of_dots_left = dot_len

    def __lt__(self, other):
        return self.position < other.get_position()

    def __eq__(self, other):
        return self.position == other.get_position() and self.number_of_dots_left == other.get_number_of_dots_left()

    def __hash__(self):
        return hash(str(self))

    def get_position(self):
        return self.position

    def set_position(position):
        self.position = position

    def get_number_of_dots_left(self):
        return self.number_of_dots_left

    def set_number_of_dots_left(self, dot_len):
        self.number_of_dots_left = dot_len
