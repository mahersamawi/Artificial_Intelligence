class Position:
	row = None
	column = None
	def __init__(self, row, column):
		self.row = row
		self.column = column

	def __eq__(self, other):
		return self.row == other.getRow() and self.column == other.getCol()

	def __neq__(self, other):
		return self.row != other.getRow() and self.column != other.getCol()

	def printPos(self):
		return "Row: " + str(self.row) + " Col: " + str(self.column)

	def getRow(self):
		return self.row
	def getCol(self):
		return self.column
	def setRow(self, row):
		self.row = row
	def setCol(self, y):
		self.column = column

