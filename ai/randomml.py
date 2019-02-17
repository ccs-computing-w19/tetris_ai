import tetris
from ai.utils.utils import isOutOfBounds
from ai.utils.pathfinding import findPath
from ai.utils.display import display

#this ai uses randomely assigned weights and biases to choose a position
#later these will be updated after training

def choosePosition(board, positions):
	return positions[0]