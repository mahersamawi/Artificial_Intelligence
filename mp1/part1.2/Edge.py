class Edge(object):
	origin = None
	dest = None
	weight = 0

	def __init__(self, first_pos, second_pos):
		self.origin = first_pos
		self.dest = second_pos
		self.weight = calc_manhattan_dist(self.origin, self.dest)

	def __eq__(self, other):
		return (self.origin == other.origin and self.dest == other.dest) or (self.dest == other.origin and self.origin == other.dest)

	def __lt__(self, other):
		return self.weight < other.weight

	def __gt__(self, other):
		return self.weight > other.weight

	def get_origin(self):
		return self.origin
	
	def get_dest(self):
		return self.dest

	def get_weight(self):
		return self.weight

	def print_edge(self):
		print("Weight: " + str(self.weight))
		print("Origin: ", end="")
		self.origin.print_pos()
		print(" Dest: ", end="")
		self.dest.print_pos()
		print("")

def calc_manhattan_dist(pos1, pos2):
    """ Function that calculates the manhattan distance of 2 positions
    Args:
        pos1: The position of the first point
        pos2: The position of the second point
    Returns:
        The manhattan distance of the 2 positions
    """
    pos1_row = pos1.get_row()
    pos1_col = pos1.get_col()

    pos2_row = pos2.get_row()
    pos2_col = pos2.get_col()

    return (abs(pos1_col - pos2_col) + abs(pos1_row - pos2_row))
