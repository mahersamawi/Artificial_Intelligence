import queue
import sys

from heapq import *
from Dot import *
from Position import *
from Node import *
from State import *
from maze_file_setup import *
from collections import deque

num_rows = None
num_cols = None


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


def get_children(current_node_state, maze_list):
    """Get the children/neighbor positions and if they are valid, append them to the children list

    Args:
        pos: the position to check if it is valid
        maze_list: the 2-D maze
    Returns:
        children: list containing valid neighbors for that position

    """
    children = []
    row = current_node_state.get_position().get_row()
    col = current_node_state.get_position().get_col()
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


def check_in_frontier(node_to_check, frontier):
    for node in frontier:
        if node_to_check.get_node_state() == node.get_node_state():
            return True
    return False

def add_to_frontier(type_of_search, obj_to_add, frontier):
    if type_of_search == "BFS":
        frontier.append(obj_to_add)


def get_from_frontier(type_of_search, frontier):
    if type_of_search == "BFS":
        top_frontier_node = frontier[0]
        frontier.popleft()
        return top_frontier_node
    else:
        return frontier.pop()


def WFS(maze_list, start_pos, dot):
    """ Function that runs DFS(stack) or BFS(queue) on the maze_list

    Args:
        maze_list: the 2-D maze
        start_pos: the starting position
        dot: the position of the dot to find

    Returns:
        child: node that is the path to the dot from the starting position
        None: Otherwise

    """
    dot_len = len(dot)

    starting_node = Node(State(start_pos, dot_len), None, 0)
    sol_path = []
    frontier = deque([])
    add_to_frontier("BFS", starting_node, frontier)
    explored = []
    while (frontier):
        frontier_node = get_from_frontier("BFS", frontier)
        explored.append(frontier_node)
        children = get_children(frontier_node.get_node_state(), maze_list)

        for loc in children:
            child = Node(State(loc, dot_len), frontier_node, 1 +
                         frontier_node.get_path_cost())

            if not (check_in_frontier(child, explored) or check_in_frontier(child, frontier)):
                if (child.get_node_state().get_position() in dot):
                    dot.remove(child.get_node_state().get_position())
                    sol_path.append(child)
                    dot_len -= 1
                    if dot_len == 0:
                        return sol_path
                add_to_frontier("BFS", child, frontier)
    return None


def goal_test(current_node):
    # check if the current node state number of dots is 0
    return (current_node.get_node_state().get_number_of_dots_left() == 0)


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

def calc_heuristic(child, dot, child_cost, a_star=False):
    if a_star:
         return (calc_manhattan_dist(child.get_position(), dot.get_position()) + child_cost)
    else:
        return (calc_manhattan_dist(child.get_position(), dot.get_position()))


# TODO
def greedy_search(maze_list, start_pos, dot, a_star=False):
    """ Function that runs greedy or a star on the maze_list
    Args:
        maze_list: the 2-D maze
        start_pos: the starting position
        dot: the position of the dot to find
        a_star: False if greedy, True if a_star
    Returns:
        child: node that is the path to the dot from the starting position
        None: Otherwise
    """
    starting_node = Node(start_pos, None, 0)

    frontier = []
    first_dist = calc_manhattan_dist(starting_node.get_position(), dot.get_position())
    first_tuple = (first_dist, starting_node)
    heappush(frontier, first_tuple)
    explored = []
    while (frontier):
        top_frontier_node = heappop(frontier)[1]
        top_frontier_pos = top_frontier_node.get_position()
        
        explored.append(top_frontier_node)
        children = get_children(top_frontier_pos, maze_list)
        # Loop through the children
        for loc in children:
            child_cost = 1 + top_frontier_node.get_path_cost()
            child = Node(loc, top_frontier_node, child_cost)
            if not (is_in_explored(child.get_position(), explored) or is_in_explored(child.get_position(), frontier, True)):
                if (child.get_position() == dot.get_position()):
                    return child
                # Add the path cost to the dist
                child_dist = calc_heuristic(child, dot, child_cost, a_star)
                child_tuple = (child_dist, child)
                heappush(frontier, child_tuple)
    return None

def loop_through_solution(sol_path, maze_list):
    cost = 0
    for i in sol_path:
        cost += i.get_path_cost()
        while i:
            # Pipe into file to get the order of nodes
            add_path_to_solution(maze_list, i)
            #i.get_node_state().get_position().print_pos()
            #print(count)
            i = i.get_parent()
    print ("Cost is " + str(cost))


def main():
    # pass in the maze and the type of search to run
    file_name = sys.argv[1]
    search_type = sys.argv[2]

    dot_list = []
    maze_list, start_pos = setup_maze(file_name, dot_list)
    global num_rows
    global num_cols
    num_rows = len(maze_list)
    num_cols = len(maze_list[0])

    if (search_type == "BFS"):
        sol_path = WFS(maze_list, start_pos, dot_list)
        loop_through_solution(sol_path, maze_list)
        print_maze_to_file(maze_list, str(search_type) + "1.2_sol_" + file_name.split("/")[-1])

    if (search_type == "a_star"):
        sol_node = greedy_search(maze_list, start_pos, dot_list, True)
        loop_through_solution(sol_node, maze_list)
        print_maze_to_file(maze_list, str(search_type) + "1.2_sol_" + file_name.split("/")[-1])

if __name__ == '__main__':
    main()
