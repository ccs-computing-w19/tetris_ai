import tetris
from ai.utils.utils import isOutOfBounds
from ai.utils.pathfinding import findPath

# return: 'best' end position
# params: game board, list of end positions
def choosePosition(board, positions):
    bestPosition = 0; bestCount = 0
    for p in range(len(positions)):
        neighborCount = 0
        for point in positions[p]:
            if isOutOfBounds(board, (point[0] - 1, point[1])) or board[point[0] - 1][point[1]].isInactive(): neighborCount += 1
            if isOutOfBounds(board, (point[0] + 1, point[1])) or board[point[0] + 1][point[1]].isInactive(): neighborCount += 1
            if isOutOfBounds(board, (point[0], point[1] - 1)) or board[point[0]][point[1] - 1].isInactive(): neighborCount += 1
            if isOutOfBounds(board, (point[0], point[1] + 1)) or board[point[0]][point[1] + 1].isInactive(): neighborCount += 1
        if neighborCount > bestCount: bestPosition = p
    position = positions[p]
    del positions[p]
    return position