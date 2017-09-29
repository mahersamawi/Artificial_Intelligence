import copy
class State(object):

    list_of_dots_left = []
    position = None

    def __init__(self, pos, dot_list):
        self.position = pos
        self.list_of_dots_left = copy.deepcopy(dot_list)

    def __lt__(self, other):
        return self.position < other.get_position()

    def __eq__(self, other):
        if self.position != other.get_position():
            return False
        
        for i in self.list_of_dots_left:
            for j in other.get_list_of_dots_left():
                if i != j:
                    return False
        return True

    def __hash__(self):
        return hash(str(self))

    def get_position(self):
        return self.position

    def set_position(position):
        self.position = position

    def get_list_of_dots_left(self):
        return self.list_of_dots_left

    def get_number_of_dots_left(self):
        return len(self.list_of_dots_left)

    def set_list_of_dots_left(self, dot_list):
        self.list_of_dots_left = copy.deepcopy(dot_list)

    def print_state(self):
        self.position.print_pos()
        print(self.list_of_dots_left)

    def remove_dot(self, pos):
        for i in self.list_of_dots_left:
            if i == pos:
                self.list_of_dots_left.remove(pos)
