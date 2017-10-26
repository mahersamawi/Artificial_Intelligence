from Flowparser import *
import random

grid, colors, src_dict = parse_flow("./flow_inputs/8x8flow.txt")
grid_bounds = len(grid[0])
count = 0
color_domain_dict = {}


def setup_man_dist_cell():
    for i in grid:
        for j in i:
            if j.is_source() is False:
                color_domain_dict[j] = get_closest_colors(j)


def get_closest_colors(cur_cell):
    # find the man dist from cur_cell to all the src cells
    color_array = []
    temp_arr = []
    # Better results with src_dict
    # as compared to colors
    for i in src_dict:
        dist1 = calc_manhattan_dist(cur_cell, src_dict[i][0])
        dist2 = calc_manhattan_dist(cur_cell, src_dict[i][1])
        color_array.append((dist1, i))
        color_array.append((dist2, i))

    color_array.sort(key=lambda tup: tup[0])
    #print(color_array)
    for i in color_array:
        if (i[1]) not in temp_arr:
            temp_arr.append(i[1])
    return temp_arr


def print_grid():
    for i in grid:
        for j in i:
            print(j, end='')
        print("")


def is_complete():
    for i in grid:
        for j in i:
            if j.get_assigned() is False:
                return False
    return True


def get_next_cell(random=False):
    if random:
        random_list = []
        for i in grid:
            for j in i:
                if j.get_assigned() is False:
                    random_list.append(j)
        return random_list
    else:
        for i in grid:
            for j in i:
                if j.get_assigned() is False:
                    return j
        return None


def pos_is_valid(row, col):
    if row >= 0 and col >= 0 and row < grid_bounds and col < grid_bounds:
        return True
    return False


def get_neighbors(cell):
    row, col = cell.get_coords()
    neighbors = []
    seen_colors = []
    if pos_is_valid(row - 1, col):
        cell = grid[row - 1][col]
        neighbors.append(cell)
        seen_colors.append(cell.get_color())
    if pos_is_valid(row + 1, col):
        cell = grid[row + 1][col]
        neighbors.append(cell)
        seen_colors.append(cell.get_color())
    if pos_is_valid(row, col - 1):
        cell = grid[row][col - 1]
        neighbors.append(cell)
        seen_colors.append(cell.get_color())
    if pos_is_valid(row, col + 1):
        cell = grid[row][col + 1]
        neighbors.append(cell)
        seen_colors.append(cell.get_color())

    return neighbors, seen_colors


def check_constraints_all():
    for i in grid:
        for j in i:
            if check_constraints(j) is False and j.get_assigned() is True:
                return False
    return True


def check_constraints(cell):
    neighbors, seen_colors = get_neighbors(cell)
    current_color = cell.get_color()
    if seen_colors.count(None) > 0:
        return True
    if cell.is_source():
        if seen_colors.count(current_color) == 1:
            return True
        return False
    for neighbor in neighbors:
        if neighbor.is_source():
            if check_constraints(neighbor) is False:
                return False
    if seen_colors.count(current_color) == 2:
        return True
    return False


def dumb_solver():
    global count
    count += 1

    if is_complete():
        return True
    current_cell = (get_next_cell())
    current_cell_colors = colors
    for color in current_cell_colors:
        prev_color = current_cell.get_color()
        prev_assignment = current_cell.get_assigned()
        current_cell.set_color(color)
        current_cell.set_assigned(True)
        if check_constraints(current_cell):
            result = dumb_solver()
            if result is not False and check_constraints_all():
                return result
        current_cell.set_color(prev_color)
        current_cell.set_assigned(prev_assignment)
    return False


def smart_solver():
    global count
    count += 1

    if is_complete():
        return True
    current_cell = (get_next_cell())
    current_cell_colors = color_domain_dict[current_cell]
    for color in current_cell_colors:
        prev_color = current_cell.get_color()
        prev_assignment = current_cell.get_assigned()
        current_cell.set_color(color)
        current_cell.set_assigned(True)
        if check_constraints(current_cell) and check_constraints_all():
            result = smart_solver()
            if result is not False and check_constraints_all():
                return result
        current_cell.set_color(prev_color)
        current_cell.set_assigned(prev_assignment)
    return False


def get_min_man_dist_src():
    final_list = []
    for src_color in src_dict:
        cur_src_dist = calc_manhattan_dist(src_dict[src_color][0], src_dict[src_color][1])
        final_list.append((src_dict[src_color][0], cur_src_dist))

    # sort list and return it
    final_list.sort(key=lambda tup: tup[1], reverse=False)

    return final_list


def calc_manhattan_dist(cell1, cell2):
    """ Function that calculates the manhattan distance of 2 positions
    Args:
        cell1: The position of the first point
        cell2: The position of the second point
    Returns:
        The manhattan distance of the 2 positions
    """
    cell1_x, cell1_y = cell1.get_position()
    cell2_x, cell2_y = cell2.get_position()
    return abs(cell1_x - cell2_x) + abs(cell1_y - cell2_y)


setup_man_dist_cell()
# for i in grid:
#     for j in i:
#         if j.is_source() is False:
#             print(color_domain_dict[j])
smart_solver()
print("Iteration: " + str(count))
print_grid()
