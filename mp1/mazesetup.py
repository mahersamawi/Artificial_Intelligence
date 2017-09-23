from Dot import *
from Position import *
from Node import *
from collections import deque

import queue

numRows = None
numCols = None


def printMaze(maze):
    for i in maze:
        print(i)


def posIsValid(pos):
    # number of rows: 23 number of columns: 61
    return (pos.getRow() >= 0 and pos.getCol() >= 0 and
            pos.getRow() < numRows and pos.getCol() < numCols)


def getChildren(pos):
    children = []
    row = pos.getRow()
    col = pos.getCol()
    print("Checking row: " + str(row) + " checking col: " + str(col))
    up = Position(row - 1, col)
    down = Position(row + 1, col)
    left = Position(row, col - 1)
    right = Position(row, col + 1)

    if(posIsValid(left)):
        children.append(left)
    if(posIsValid(right)):
        children.append(right)
    if(posIsValid(up)):
        children.append(up)
    if(posIsValid(down)):
        children.append(down)

    print("Children length: " + str(len(children)))
    return children


def isInExplored(pos, explored):
    for loc in explored:
        if loc.__eq__(pos):
            return True
    return False


def WFS(maze_list, start_pos, dot, type_of_search):
    starting_node = Node(start_pos, None, 0)
    if (starting_node.getPosition().__eq__(dot.getPosition())):
        return 0
    if type_of_search == "BFS":
        frontier_pos = deque([])
        frontier_node = deque([])
    else:
        frontier_pos = []
        frontier_node = []
    frontier_pos.append(starting_node.getPosition())
    frontier_node.append(starting_node)
    explored = []
    while (frontier_pos):
        print("Number of nodes visited: " + str(len(explored)))
        print("Frontier size: " + str(len(frontier_pos)))
        if type_of_search == "BFS":
            top_frontier_pos = frontier_pos[0]
            top_frontier_node = frontier_node[0]
            frontier_pos.popleft()
            frontier_node.popleft()
        else:
            top_frontier_pos = frontier_pos.pop()
            top_frontier_node = frontier_node.pop()
        explored.append(top_frontier_pos)
        children = getChildren(top_frontier_pos)

        for loc in children:
            child = Node(loc, top_frontier_node, 1 +
                         top_frontier_node.getPathCost())

            if not (isInExplored(child.getPosition(), explored) or isInExplored(child.getPosition(), frontier_pos)):
                print("CHILD: " + child.getPosition().printPos() +
                      " DOT: " + dot.getPosition().printPos())

                if (child.getPosition().__eq__(dot.getPosition())):
                    print("SUCCESS")
                    return 1 + top_frontier_node.getPathCost()
                frontier_pos.append(child.getPosition())
                frontier_node.append(child)


def main():
    file_name = "mediumMaze.txt"

    maze_list = None
    dot_list = []

    state = None
    start_pos = None

    with open(file_name) as textFile:
        maze_list = [[str(c) for c in line.rstrip()] for line in textFile]

    print(len(maze_list))
    for i in range(len(maze_list)):
        for j in range(len(maze_list[i])):
            if (maze_list[i][j] == 'P'):
                start_pos = Position(i, j)
            elif (maze_list[i][j] == '.'):
                dot_list.append(Dot(Position(i, j)))

    global numRows
    global numCols
    numRows = len(maze_list)
    numCols = len(maze_list[0])
    for dot in dot_list:
        print("Dot row: " + str(dot.getPosition().getRow()) +
              " Dot col: " + str(dot.getPosition().getCol()))

    print("Start row: " + str(start_pos.getRow()) +
          " Start col: " + str(start_pos.getCol()))

    # input BFS or DFS
    search = "BFS"
    print(WFS(maze_list, start_pos, dot_list[0], search))


if __name__ == '__main__':
    main()
