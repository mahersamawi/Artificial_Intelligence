class Node(object):
    """Node class that contains the parent node, the node's location and cost

    Attributes:
        position (Position object): Position object for the Node
        parent (Node object): Parent node of the node
        path_cost (int): Cost to get to this node from the starting node

    """
    node_state = None
    parent = None
    path_cost = None

    def __init__(self, current_state, parent, path_cost):
        self.node_state = current_state
        self.parent = parent
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.get_path_cost()

    def __eq__(self, other):
        return (self.node_state == other.get_node_state() and self.path_cost == other.get_path_cost())

    def __hash__(self):
        return hash((self.node_state, self.path_cost))

    def get_node_state(self):
        return self.node_state

    def set_node_state(self, current_state):
        self.node_state = current_state

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_path_cost(self):
        return self.path_cost

    def set_path_cost(self, path_cost):
        self.path_cost = path_cost

    def print_node_state(self):
        self.node_state.print_state()
