import sys
from Dot import *
from Position import *
from Node import *

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


def print_maze_to_file(maze, out_file):
    """Prints the maze to the out_file
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