from Cell import *


def parse_flow(file_name):
    src_dict = {}
    with open(file_name) as text_file:
        flow_grid = [[str(c) for c in line.rstrip()] for line in text_file]
    color_list = []
    for i in range(len(flow_grid)):
        for j in range(len(flow_grid[i])):
            color = flow_grid[i][j]
            if color == '_':
                flow_grid[i][j] = Cell(i, j, None)
            else:
                src_cell = Cell(i, j, color)
                flow_grid[i][j] = src_cell
                if color not in src_dict:
                    src_dict[color] = [src_cell]
                else:
                    src_dict[color].append(src_cell)
                if color not in color_list:
                    color_list.append(color)

    return flow_grid, color_list, src_dict
