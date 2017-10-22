from Flowparser import *
from Cell import *

grid, colors = parse_flow("./flow_inputs/5x5flow.txt")
grid_bounds = len(grid[0])
count = 0

def print_grid():
	for i in grid:
		for j in i:
			print(j, end='')
		print("")

def is_complete():
	for i in grid:
		for j in i:
			if check_constraints(j) == False and not j.is_source():
				print("Setting back to unassigned")
				j.print_position()
				j.set_color(None)
				j.set_assigned(False)
				return False
			if j.get_assigned() == False:
				return False
	return True

def get_next_cell():
	for i in grid:
		for j in i:
			if (j.get_assigned() == False):
				print("Getting next cell")
				j.print_position()
				return j
	return None

def pos_is_valid(row, col):
    if (row >= 0 and col >= 0 and row < grid_bounds and col < grid_bounds):
        return True
    return False

def get_neighbors(cell):
	row, col = cell.get_coords()
	neighbors = []
	seen_colors = []
	if(pos_is_valid(row-1, col)):
		cell = grid[row-1][col]
		neighbors.append(cell)
		seen_colors.append(cell.get_color())
	if(pos_is_valid(row+1, col)):
		cell = grid[row+1][col]
		neighbors.append(cell)
		seen_colors.append(cell.get_color())
	if(pos_is_valid(row, col-1)):
		cell = grid[row][col-1]
		neighbors.append(cell)
		seen_colors.append(cell.get_color())
	if(pos_is_valid(row, col+1)):
		cell = grid[row][col+1]
		neighbors.append(cell)
		seen_colors.append(cell.get_color())

	return neighbors, seen_colors


def check_constraints(cell):
	neighbors, seen_colors = get_neighbors(cell)
	current_color = cell.get_color()
	if (seen_colors.count(None) > 0):
		return True
	if (cell.is_source()):
		# cell.print_position()
		if (seen_colors.count(current_color) == 1):
			# print("checkpoint 1")
			return True
		return False
	for neighbor in neighbors:
		if (neighbor.is_source() == True):
			if (check_constraints(neighbor) == False):
				# print("checkpoint 2")
				return False
	if (seen_colors.count(current_color) == 2):
		# print("checkpoint 3")
		return True
	# print("checkpoint 4")	
	return False


def dumb_solver():
	global count
	print("Iteration: " + str(count))
	count += 1
	
	current_cell = get_next_cell()
	if is_complete():
		return True
	current_cell = get_next_cell()
	current_pos = current_cell.get_position()
	#current_cell.print_position()

	for color in colors:
		current_cell.set_color(color)
		current_cell.set_assigned(True)
		if (check_constraints(current_cell) == True):
			result = dumb_solver()
			if (result != False and is_complete()):
				print("SUCCESS")
				# print(is_complete())
				return result
	return False

dumb_solver()
print_grid()
