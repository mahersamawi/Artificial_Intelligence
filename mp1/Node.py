class Node(object):
    """Node class that contains the parent node, the node's location and cost

    Attributes:
        position (Position object): Position object for the Node
        parent (Node object): Parent node of the node
        path_cost (int): Cost to get to this node from the starting node

    """
    position = None
    parent = None
    path_cost = None

    def __init__(self, pos, parent, path_cost):
        self.position = pos
        self.parent = parent
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.position < other.get_position()

    def get_position(self):
        return self.position

    def set_position(position):
        self.position = position

    def get_parent(self):
        return self.parent

    def set_parent(parent):
        self.parent = parent

    def get_path_cost(self):
        return self.path_cost

    def set_path_cost(path_cost):
        self.path_cost = path_cost
