import tetris, copy

def print_out(board):
    for i in range(len(board)):
        string = ""
        for j in range(len(board[i])):
            string += str(board[i][j].state)
        print(string)

# return: start point rotated around pivot point (clockwise)
# params: start point, pivot point
def rotate(point, pivot):
    return (point[1] - pivot[1] + pivot[0], pivot[0] - point[0] + pivot[1], (point[2] + 1) % 4)

def rotateReverse(point, pivot):
    return (pivot[0] + pivot[1] - point[1], point[0] + pivot[1] - pivot[0], (point[2] - 1) % 4)

# return: position of active piece
# params: game board
def getActivePosition(board, pivot):
    position = []
    if pivot != (-1, -1):
        position.append((pivot[0], pivot[1], 0))
    for i in range(len(board)):
        for j in range(len(board[i])):
            if not (i == pivot[0] and j == pivot[1]): # make sure it isn't pivot
                if board[i][j].state == 2: position.append((i, j, 0))
            # position[2] is the rotation, which is default, so 0
    return position

# return: list of valid end positions
# params: game board, if the piece is rotatable
def findPositions(board, tiles, rotatable):
    # find every translation and rotation of the initial position:
    arrangements = []
    for i in range(-tiles[0][0], -tiles[0][0] + len(board)):
        for j in range(-tiles[0][1], -tiles[0][1] + len(board[i])):
            # rotation is communitive, any pivot can be used
            arrangement = []
            for k in range(len(tiles)):
                point = (i + tiles[k][0], j + tiles[k][1], 0)
                arrangement.append(point)
            arrangements.append(arrangement)
            if rotatable: # is rotatable
                for r in range(1, 4): # for each rotation
                    arrangement = copy.copy(arrangements[-1])
                    pivot = arrangement[0]
                    for k in range(len(arrangement)):
                        arrangement[k] = rotate(arrangement[k], pivot)
                    arrangements.append(arrangement)
    # prune arrangements if they are invalid:
    # meaning that they must be
    # 1) within the bounds of the board
    # 2) unable to be moved downwards (I.E. on the bottom)
    # 3) not a duplicate of another valid arrangement
    pruned = []
    for arrangement in arrangements:
        valid = True
        for point in arrangement:
            if point[0] < 0 or point[0] >= len(board) or point[1] < 0 or point[1] >= len(board[0]) or board[point[0]][point[1]].isInactive():
                valid = False; break
        if valid: # if it is still valid
            for point in arrangement:
                # test if point is on bottom:
                if point[0] == len(board) - 1 or board[point[0] + 1][point[1]].isInactive():
                    # check to see if arrangement is a duplicate:
                    #pruned.append(arrangement)
                    isDuplicate = False
                    for prune in pruned:
                        sameAsPrune = True
                        rotation = prune[0][2] # get rotation number
                        for point in arrangement:
                            if (point[0], point[1], rotation) not in prune:
                                #print("This:", (point[0], point[1], rotation))
                                #print("not in this:", prune)
                                #print("so add this:", arrangement)
                                sameAsPrune = False; break
                        if sameAsPrune:
                            isDuplicate = True; break
                    if not isDuplicate:
                        pruned.append(arrangement); break
    return pruned

import os
def print_out(board, position):
    os.system('clear')
    string = []
    for i in range(len(board)):
        string.append([])
        for j in range(len(board[i])):
            string[i].append("." if board[i][j].state == 0 else "o")
    for point in position:
        string[point[0]][point[1]] = "*"
    for i in string:
        print("".join(i))
    
    

# return: series of moves ['d', 'd', 'r', 'r', 'r', 'l', 'l', 'l', 'd']
# params: game board, final position of piece
def findPath(board, position, target, rotatable):
    visited = []
    print_out(board, target)
    return recFindPath(board, position, target, rotatable, visited)

def recFindPath(board, position, target, rotatable, visited, left=False, right=False, rotated=0):
    # print for debugging:
    #if (validPosition(board, position, target)):
    #    print_out(board, position, target)
    
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

# return if the positions are the same
def comparePosition(position, prime):
    for p in range(len(position)):
        if position[p][0] != prime[p][0] or position[p][1] != prime[p][1]:
            return False
    return True

def validPosition(board, position, target):
    for point in target:
        if point[0] < 0 or point[1] < 0 or point[0] >= len(board) or point[1] >= len(board[0]):
            return False
        if board[point[0]][point[1]].isInactive():
            return False
    if target[0][0] < position[0][0]: # if the target is above the position
        return False
    return True

def translateUp(position):
    prime = []
    for point in position:
        prime.append((point[0] - 1, point[1], point[2]))
    return prime

def translateLeft(position):
    prime = []
    for point in position:
        prime.append((point[0], point[1] - 1, point[2]))
    return prime

def translateRight(position):
    prime = []
    for point in position:
        prime.append((point[0], point[1] + 1, point[2]))
    return prime

def rotateRight(position, pivot):
    prime = []
    for point in position:
        prime.append(rotateReverse(point, pivot))
    return prime

def rotateLeft(position, pivot):
    pass


