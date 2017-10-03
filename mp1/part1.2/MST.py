from Edge import *
def get_list_of_edges(dot_list, edge_list):
	for i in range(len(dot_list)):
		for j in range(i, len(dot_list)):
			if (i != j):
				global all_edges
				edge_list.append(Edge(dot_list[i], dot_list[j]))

# partially derived from 
# https://github.com/israelst/Algorithms-Book--Python/blob/master/5-Greedy-algorithms/kruskal.py
def check_if_covered(new_pos, positions_covered):
	for pos in positions_covered:
		if pos == new_pos:
			return True
	return False

def print_edges(edge_list):
	print("Edge length: " + str(len(edge_list)))
	i = 1
	for edge in edge_list:
		print("Edge " + str(i))
		edge.print_edge()
		i += 1
		print("")    

def find(dot, parent):
	if parent[dot] != dot:
		parent[dot] = find(parent[dot], parent)
	return parent[dot]

def union(dot1, dot2, parent_dict, rank_dict):
	root1 = find(dot1, parent_dict)
	root2 = find(dot2, parent_dict)
	if root1 != root2:
		if rank_dict[root1] > rank_dict[root2]:
			parent_dict[root2] = root1
		else:
			parent_dict[root1] = root2
			if rank_dict[root1] == rank_dict[root2]: rank_dict[root2] += 1

def get_MST(dot_list):
	all_edges = []
	MST = []
	positions_covered = []
	num_vertices = len(dot_list)

	parent_dict = {}
	rank_dict = {}
	for dot in dot_list:
		parent_dict[dot] = dot
		rank_dict[dot] = 0

	get_list_of_edges(dot_list, all_edges)
	all_edges.sort(key=lambda x: x.weight, reverse=False)
	# print_edges(all_edges)

	for edge in all_edges:
		if (len(MST) == (num_vertices - 1)):
			break
		origin = edge.get_origin()
		dest = edge.get_dest()
		if find(origin, parent_dict) != find(dest, parent_dict):
			union(origin, dest, parent_dict, rank_dict)
			MST.append(edge)
		# if not (check_if_covered(origin, positions_covered) and check_if_covered(dest, positions_covered)):
		#   MST.append(edge)
		#   positions_covered.append(origin)
		#   positions_covered.append(dest)
	# print_edges(MST)


	return MST
