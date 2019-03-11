from ai.utils.utils import isOutOfBounds
from ai.utils.pathfinding import findPath
from ai.utils.display import display
from ml.utils.heuristics import *

# This ai uses pretrained weights for height, neighbors, holes

# return: 'best' end position
# params: game board, list of end positions

def openModel():
	f = open("ml/model", 'r')
	wHeight = float(f.readline())
	wNeighbors = float(f.readline())
	wHoles = float(f.readline())
	return [wHeight, wNeighbors, wHoles]

def choosePosition(board, positions, weights=[]):
	if len(weights) == 0: weights = openModel()
	bestPosScore = weights[0] * findHeight(board) + weights[1] * numOfNeighbors(positions[0], board) + weights[2] * numOfHoles(positions[0], board)
	bestPosIndex = 0
	for p in range(1, len(positions)):
		score = weights[0] * findHeight(board) + weights[1] * numOfNeighbors(positions[p], board) + weights[2] * numOfHoles(positions[p], board)
		if score >= bestPosScore:
			bestPosScore = score
			bestPosIndex = p
	return bestPosIndex