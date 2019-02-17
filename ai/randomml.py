import tetris
from ai.utils.utils import isOutOfBounds
from ai.utils.pathfinding import findPath
from ai.utils.display import display

#this ai uses randomely assigned weights and biases to choose a position
#later these will be updated after training

#choose weights for
#	height
#	lowest hole
#	holes
#	filled lines (clear)
#	touching neighbors

def choosePosition(board, positions):
	return positions[0]

def height(board, position):
	pass

def lowest(board, position):
	pass

def holes(board, position):
	pass

def clears(board, posiiton):
	pass

def neighbors(board, position):
	pass

def numWells(board, position):
	pass
