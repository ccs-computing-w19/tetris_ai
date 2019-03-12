from ai.utils.utils import isOutOfBounds
from ai.utils.pathfinding import findPath
from ai.utils.display import display
from ml.utils.heuristics import *

# This ai uses pretrained weights for height, neighbors, holes

# return: 'best' end position
# params: game board, list of end positions

def openModel():
	weights = open("ml/model", 'r').read().strip().split()
	return [float(weight.strip()) for weight in weights] # convert string weights to floating point numbers

def choosePosition(board, positions, weights=[]):
	if len(weights) == 0: weights = openModel()
	bestPosScore = weights[0] * lineClears(positions[0], board) + weights[1] * numOfNeighbors(positions[0], board) + weights[2] * numOfHoles(positions[0], board) + weights[3] * pieceHeight(positions[0], board)
	bestPosIndex = 0
	for p in range(1, len(positions)):
		score = weights[0] * lineClears(positions[p], board) + weights[1] * numOfNeighbors(positions[p], board) + weights[2] * numOfHoles(positions[p], board) + weights[3] * pieceHeight(positions[p], board)
		#print(round(score,2), findHeight(board), numOfNeighbors(positions[p], board), numOfHoles(positions[p], board), pieceHeight(positions[p], board))
		if score >= bestPosScore:
			bestPosScore = score
			bestPosIndex = p
	#print("BEST:", round(bestPosScore,2))
	return bestPosIndex