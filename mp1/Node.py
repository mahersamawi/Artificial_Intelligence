class Node:
	position = None
	parent = None
	path_cost = None
	def __init__(self, pos, parent, path_cost):
		self.position = pos
		self.parent = parent
		self.path_cost = path_cost

	def getPosition(self):
		return self.position
	def setPosition(position):
		self.position = position
	def getParent(self):
		return self.parent
	def setParent(parent):
		self.parent = parent
	def getPathCost(self):
		return self.path_cost
	def setPathCost(path_cost):
		self.path_cost = path_cost