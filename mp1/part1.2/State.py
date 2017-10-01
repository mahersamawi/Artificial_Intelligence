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
        if isinstance(other, self.__class__):
            if self.position != other.get_position():
                return False
            if self.get_number_of_dots_left() != other.get_number_of_dots_left():
                return False   
            return set(get_list_of_dots_left) == set(other.get_list_of_dots_left())
            # list1 = self.list_of_dots_left
            # list2 = other.get_list_of_dots_left()
            # for i in range(0, len(list1)):
            #     for j in range(0, len(list2)):
            #         if (list1[i] == list2[j]):
            #             break
            #         if (j == (len(list2) - 1)):

            #             return False
            # print("States are the same!")
            return True
        else:
            print("State objects not the same!")
            return False

    def __hash__(self):
        return hash((self.position, tuple(self.list_of_dots_left)))

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
        print("Current position: ") 
        self.position.print_pos()
        print("\n")
        print("Dot list: ")
        for i in self.list_of_dots_left:
            print(" Dot: ", end="")
            i.print_pos()
        print("\n")


    def remove_dot(self, pos):
        for i in self.list_of_dots_left:
            if i == pos:
                self.list_of_dots_left.remove(pos)
