import tetris
from ai.utils.utils import *
#from ai.utils.display import display

# return: series of moves ['d', 'd', 'r', 'r', 'r', 'l', 'l', 'l', 'd']
# params: game board, final position of piece
def findPath(board, position, target, rotatable):
    visited = []
    #display(board, target)
    #fixing bugs:
    return recFindPath(board, position, target, rotatable, visited)

"""
def recFindPath(board, position, target, rotatable, visited, left=False, right=False, rotated=0):
    if comparePosition(position, target):
        return []
    if not validPosition(board, position, target):
        return
    if target in visited:
        return
    if rotated > 3:
        return
    result = recFindPath(board, position, translateUp(target), rotatable, visited)
    if result != None:
        return result + ['d']
    if not right:
        result = recFindPath(board, position, translateLeft(target), rotatable, visited, left=True)
        if result != None:
            return result + ['r']
    if not left:
        result = recFindPath(board, position, translateRight(target), rotatable, visited, right=True)
        if result != None:
            return result + ['l']
    if rotatable:
        result = recFindPath(board, position, rotateRight(target, target[0]), rotatable, visited, left=left, right=right, rotated=rotated+1)
        if result != None:
            return result + ['u']
    if target not in visited:
        visited.append(target)
    return
"""

def recFindPath(board, position, target, rotatable, visited, left=False, right=False, rotated=0):
    if comparePosition(position, target):
        return []
    if not validPosition(board, position, target):
        return
    if target in visited:
        return
    if rotated > 3:
        return
    result = recFindPath(board, position, translateUp(target), rotatable, visited)
    if result != None:
        return result + ['d']
    if rotatable:
        result = recFindPath(board, position, rotateRight(target, target[0]), rotatable, visited, left=left, right=right, rotated=rotated+1)
        if result != None:
            return result + ['u']
    if not right:
        result = recFindPath(board, position, translateLeft(target), rotatable, visited, left=True)
        if result != None:
            return result + ['r']
    if not left:
        result = recFindPath(board, position, translateRight(target), rotatable, visited, right=True)
        if result != None:
            return result + ['l']
    if target not in visited:
        visited.append(target)
    return