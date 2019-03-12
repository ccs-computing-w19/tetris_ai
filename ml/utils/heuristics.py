from ai.utils.utils import getActivePosition, findPositions, isOutOfBounds
from ai.utils.pathfinding import findPath
from ai.utils.display import display

def lineClears(position, board):
    clears = []
    for point in position:
        if point[0] not in clears:
            rowIsFull = True
            for col in range(len(board[point[0]])):
                if board[point[0]][col].isEmpty() and (point[0], col, point[2]) not in position:
                    rowIsFull = False
            if rowIsFull:
                clears.append(point[0])
    return len(clears)


def numOfNeighbors(position, board):
    neighborCount = 0
    for point in position:
        if isOutOfBounds(board, (point[0] - 1, point[1])) or board[point[0] - 1][point[1]].isInactive(): neighborCount += 1
        if isOutOfBounds(board, (point[0] + 1, point[1])) or board[point[0] + 1][point[1]].isInactive(): neighborCount += 1
        if isOutOfBounds(board, (point[0], point[1] - 1)) or board[point[0]][point[1] - 1].isInactive(): neighborCount += 1
        if isOutOfBounds(board, (point[0], point[1] + 1)) or board[point[0]][point[1] + 1].isInactive(): neighborCount += 1
    return neighborCount

def numOfHoles(position, board):
    holeCount = 0
    for point in position:
        if (not isOutOfBounds(board, (point[0] + 1, point[1])) and not (point[0] + 1, point[1], point[2]) in position and not board[point[0] + 1][point[1]].isInactive()):
            holeCount += 1
    return holeCount

def pieceHeight(position, board):
    return position[0][0]