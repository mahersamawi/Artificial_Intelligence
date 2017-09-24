import queue

from Dot import *
from Position import *
from Node import *
from collections import deque

num_rows = None
num_cols = None


def add_path_to_solution(maze, cur_node):
    """Puts the "." in the maze for the solution path

    Args:
        maze: the 2-D maze 
        cur_node: the node whose position will be marked with "." in the maze
    Returns:
        Nothing

    """
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            row = cur_node.get_position().get_row()
            col = cur_node.get_position().get_col()
            if i == row and j == col:
                maze[i][j] = "."


def print_maze_to_file(maze, out_file):
    """Prints the maze to file

    Args:
        maze: the 2-D maze 
        out_file: the name of the file to write to
    Returns:
        Nothing

    """
    with open(out_file, "w") as text_file:
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                text_file.write(maze[i][j])
            text_file.write("\n")


def pos_is_valid(pos, maze_list):
    """Checks to see if the position is valid and not a wall

    Args:
        pos: the position to check if it is valid
        maze_list: the 2-D maze 
    Returns:
        True: if the position is a valid one
        False: Otherwise

    """
    row = pos.get_row()
    col = pos.get_col()
    if (row >= 0 and col >= 0 and row < num_rows and col < num_cols):
        if maze_list[row][col] == "%":
            return False
        return True
    return False


def get_children(pos, maze_list):
    """Get the children/neighbor positions and if they are valid, append them to the children list 

    Args:
        pos: the position to check if it is valid
        maze_list: the 2-D maze 
    Returns:
        children: list containing valid neighbors for that position

    """
    children = []
    row = pos.get_row()
    col = pos.get_col()
    up = Position(row - 1, col)
    down = Position(row + 1, col)
    left = Position(row, col - 1)
    right = Position(row, col + 1)

    if(pos_is_valid(left, maze_list)):
        children.append(left)
    if(pos_is_valid(right, maze_list)):
        children.append(right)
    if(pos_is_valid(up, maze_list)):
        children.append(up)
    if(pos_is_valid(down, maze_list)):
        children.append(down)

    return children


def is_in_explored(pos, explored):
    """Checks to see if pos is in the explored list by comparing the row and column 
        of each position rather than the objects

    Args:
        pos: the position to check if it is valid
        explored: list of visited positions
    Returns:
        True: if the position is in the explored list
        False: Otherwise

    """
    for loc in explored:
        if loc.equals(pos):
            return True
    return False


def WFS(maze_list, start_pos, dot, type_of_search):
    """ Function that runs DFS(stack) or BFS(queue) on the maze_list 

    Args:
        maze_list: the 2-D maze 
        start_pos: the starting position
        dot: the position of the dot to find
        type_of_search: BFS or DFS depending on the search 

    Returns:
        child: node that is the path to the dot from the starting position
        None: Otherwise

    """
    starting_node = Node(start_pos, None, 0)
    if (starting_node.get_position().equals(dot.get_position())):
        return 0
    if type_of_search == "BFS":
        frontier_pos = deque([])
        frontier_node = deque([])
    else:
        frontier_pos = []
        frontier_node = []
    frontier_pos.append(starting_node.get_position())
    frontier_node.append(starting_node)
    explored = []
    while (frontier_pos):
        if type_of_search == "BFS":
            top_frontier_pos = frontier_pos[0]
            top_frontier_node = frontier_node[0]
            frontier_pos.popleft()
            frontier_node.popleft()
        else:
            top_frontier_pos = frontier_pos.pop()
            top_frontier_node = frontier_node.pop()
        explored.append(top_frontier_pos)
        children = get_children(top_frontier_pos, maze_list)

        for loc in children:
            child = Node(loc, top_frontier_node, 1 +
                         top_frontier_node.get_path_cost())

            if not (is_in_explored(child.get_position(), explored) or is_in_explored(child.get_position(), frontier_pos)):
                if (child.get_position().equals(dot.get_position())):
                    return child
                frontier_pos.append(child.get_position())
                frontier_node.append(child)
    return None


def setup_maze(file_name, dot_list):
    """ Function that sets up maze by populating maze_list, dot_list and start_pos

    Args:
        file_name: name of file that contains the unsolved maze
        dot_list: list containing the positions of the dots
    Returns:
        Tuple containing
        maze_list: the 2-D maze that stores the maze  
        start_pos: the starting position of the maze

    """
    with open(file_name) as text_file:
        maze_list = [[str(c) for c in line.rstrip()] for line in text_file]

    for i in range(len(maze_list)):
        for j in range(len(maze_list[i])):
            if (maze_list[i][j] == 'P'):
                start_pos = Position(i, j)
            elif (maze_list[i][j] == '.'):
                dot_list.append(Dot(Position(i, j)))
    return maze_list, start_pos


def main():
    file_name = "bigMaze.txt"
    dot_list = []
    maze_list, start_pos = setup_maze(file_name, dot_list)
    global num_rows
    global num_cols
    num_rows = len(maze_list)
    num_cols = len(maze_list[0])

    # input BFS or DFS
    search = "DFS"
    cur_node = (WFS(maze_list, start_pos, dot_list[0], search))
    while cur_node:
        add_path_to_solution(maze_list, cur_node)
        cur_node = cur_node.get_parent()
    print_maze_to_file(maze_list, "out_DFS.txt")


if __name__ == '__main__':
    main()
