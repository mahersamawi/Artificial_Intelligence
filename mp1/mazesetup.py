from Dot import *
from Position import *
from Node import *

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


def getChildren(pos, maze_list):
    children = []
    row = pos.getRow()
    col = pos.getCol()
    print("Checking row: " + str(row) + " checking col: " + str(col))
    up = Position(row - 1, col)
    down = Position(row + 1, col)
    left = Position(row, col - 1)
    right = Position(row, col + 1)

    if(posIsValid(up)):
        children.append(up)
    if(posIsValid(down)):
        children.append(down)
    if(posIsValid(left)):
        children.append(left)
    if(posIsValid(right)):
        children.append(right)

    print("Children length: " + str(len(children)))
    return children


def isInExplored(pos, explored):
    for loc in explored:
        # print("First: " + pos.printPos() + " Second: " + loc.printPos())
        if loc.__eq__(pos):
            return True
    return False


def BFS(maze_list, start_pos, dot):
    starting_node = Node(start_pos, None, 0)
    if (starting_node.getPosition().__eq__(dot.getPosition())):
        return 0
    frontier = queue.Queue(0)
    frontier.put(starting_node)
    explored = []
    while not (frontier.empty()):
        print("Number of nodes visited: " + str(len(explored)))
        print("Frontier size: " + str(frontier.qsize()))
        top_frontier = frontier.get()
        explored.append(top_frontier.getPosition())
        children = getChildren(top_frontier.getPosition(), maze_list)
        for loc in children:
            child = Node(loc, top_frontier, 1 + top_frontier.getPathCost())
            if (not (isInExplored(child.getPosition(), explored)) or not (child in frontier.queue)):
                print("CHILD: " + child.getPosition().printPos() +
                      " DOT: " + dot.getPosition().printPos())
                if (child.getPosition().__eq__(dot.getPosition())):
                    print("SUCCESS")
                    return 1 + top_frontier.getPathCost()
                frontier.put(child)


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

    print(BFS(maze_list, start_pos, dot_list[0]))


if __name__ == '__main__':
    main()
