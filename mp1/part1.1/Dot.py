class Dot(object):
    """Dot class that contains the position of the dot from the maze
    Attributes:
        position (Position object): Position object for the Dot
    """
    position = None

    def __init__(self, pos):
        self.position = pos

    def get_position(self):
        return self.position

    def set_position(position):
        self.position = position