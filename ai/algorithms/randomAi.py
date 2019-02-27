from random import randint
from ai.utils.utils import *
from ai.utils.pathfinding import findPath

# return: 'best' end position
# params: game board, list of end positions
def choosePosition(board, positions):
    return randint(0, len(positions) - 1)