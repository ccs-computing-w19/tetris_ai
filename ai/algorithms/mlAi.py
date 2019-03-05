from ai.utils.utils import isOutOfBounds
from ai.utils.pathfinding import findPath
from ai.utils.display import display

# This ai uses pretrained weights for height, neighbors, holes

# return: 'best' end position
# params: game board, list of end positions

def findHeight(board):
	height = 0
	for r in range(len(board)):
		if(1 in board[r]):
			height = len(board) - r
			break
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

def choosePosition(board, positions):
	f = open("mlmodel", 'r')
	wHeight = float(f.readline())
	wNeighbors = float(f.readline())
	wHoles = float(f.readline())

	positionScores = []
	bestPosIndex = -1
	for pos in positions:
		positionScores.append(wHeight * findHeight(board) + wNeighbors * numOfNeighbors(pos, board) + wHoles * numOfHoles(pos, board))
	bestPosScore = max(positionScores)
	numOfPositions = len(positions)
	for i in range(numOfPositions):
		if(positionScores[i] == bestPosScore):
			bestPosIndex = i
	return bestPosIndex