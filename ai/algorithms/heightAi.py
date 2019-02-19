import tetris
from ai.utils.utils import isOutOfBounds
from ai.utils.pathfinding import findPath
from ai.utils.display import display

# This ai chooses the position that gives the lowest height
def choosePosition(board, positions):
	bestPosition = 0
	bestPart = [0]

	for p in range(len(positions)):
		for part in positions[p]:
			if(part[0] > bestPart[0]):
				if(not isOutOfBounds(board, part)):
					bestPosition = p
					bestPart = part
				break
	#print(bestPart)
	#print(bestPosition)
	position = positions[bestPosition]
	del positions[bestPosition]
	return position