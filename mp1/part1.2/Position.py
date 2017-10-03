class Position(object):
    """Attributes:
        row (int): row location of the object
        column (int): column location of the object

    """
    row = None
    column = None

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __lt__(self, other):
        return self.row < other.get_row() 

    def __eq__(self, other):
        return self.row == other.get_row() and self.column == other.get_col()
        # else:
        #     print("Position objects not the same!")
        #     return False

    def __hash__(self):
        return hash((self.row, self.column))

    def __ne__(self, other):
        return self.row != other.get_row() or self.column != other.get_col()

    def print_pos(self):
        print (" Row: " + str(self.row) + " Col: " + str(self.column), end = "")

    def get_row(self):
        return self.row

    def get_col(self):
        return self.column

    def set_row(self, row):
        self.row = row

    def set_col(self, y):
        self.column = column
