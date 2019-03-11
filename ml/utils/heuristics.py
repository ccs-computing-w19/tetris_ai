from ai.utils.utils import getActivePosition, findPositions, isOutOfBounds
from ai.utils.pathfinding import findPath
from ai.utils.display import display

def findHeight(board):
    height = 3
    for r in range(len(board)):
        for tile in board[r]:
            if tile.isInactive(): return len(board) - r
    return height

def numOfNeighbors(position, board):
    neighborCount = 0
    for point in position:
        if isOutOfBounds(board, (point[0] - 1, point[1])) or board[point[0] - 1][point[1]].isInactive(): neighborCount += 1
        if isOutOfBounds(board, (point[0] + 1, point[1])) or board[point[0] + 1][point[1]].isInactive(): neighborCount += 1
        if isOutOfBounds(board, (point[0], point[1] - 1)) or board[point[0]][point[1] - 1].isInactive(): neighborCount += 1
        if isOutOfBounds(board, (point[0], point[1] + 1)) or board[point[0]][point[1] + 1].isInactive(): neighborCount += 1
    return neighborCount

def numOfHoles(position, board):
    holes = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if(not isOutOfBounds(board, (r - 1, c)) and board[r-1][c].isInactive()):
                holes += 1
    return holes

def pieceHeight(position, board):
    return position[0][0]