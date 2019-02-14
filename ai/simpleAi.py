import tetris
from ai.utils.utils import *
from ai.utils.pathfinding import findPath

# return: 'best' end position
# params: game board, list of end positions
def choosePosition(board, positions):
    p = -1 # naïvely choose the last position
    # remove the selected position
    position = positions[p]
    del positions[p]
    return position
