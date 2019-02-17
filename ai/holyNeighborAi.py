import tetris
from ai.utils.utils import isOutOfBounds
from ai.utils.pathfinding import findPath
from ai.utils.display import display

# This ai tries to maximize the number of occupied tiles that border the target

#Weights:
HOLE = -3
NEIGHBOR = 1
DEPTH = 3 #inverse

# return: 'best' end position
# params: game board, list of end positions
def choosePosition(board, positions):
    #display(board)
    #print("START")
    bestPosition = 0; bestCount = -100
    for p in range(len(positions)):
        neighborCount = positions[p][0][0] // DEPTH
        for point in positions[p]:
            if isOutOfBounds(board, (point[0] - 1, point[1])) or board[point[0] - 1][point[1]].isInactive(): neighborCount += NEIGHBOR
            if isOutOfBounds(board, (point[0] + 1, point[1])) or board[point[0] + 1][point[1]].isInactive(): neighborCount += NEIGHBOR
            elif board[point[0] + 1][point[1]].isEmpty() and (point[0] + 1, point[1], point[2]) not in positions[p]: neighborCount += HOLE
            if isOutOfBounds(board, (point[0], point[1] - 1)) or board[point[0]][point[1] - 1].isInactive(): neighborCount += NEIGHBOR
            if isOutOfBounds(board, (point[0], point[1] + 1)) or board[point[0]][point[1] + 1].isInactive(): neighborCount += NEIGHBOR
        if neighborCount >= bestCount: 
            bestPosition = p
            bestCount = neighborCount
    position = positions[bestPosition]
    del positions[bestPosition]
    return position