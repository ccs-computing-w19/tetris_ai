import tetris, copy

#                               #
#     UTILITIES FOR POINTS      #
#                               #

# return: start point rotated around pivot point (clockwise)
# params: start point, pivot point
def rotate(point, pivot):
    return (point[1] - pivot[1] + pivot[0], pivot[0] - point[0] + pivot[1], (point[2] + 1) % 4)

def rotateReverse(point, pivot):
    return (pivot[0] + pivot[1] - point[1], point[0] + pivot[1] - pivot[0], (point[2] - 1) % 4)

# checks if a point is in bounds
def isOutOfBounds(board, point):
    return point[0] < 0 or point[1] < 0 or point[0] >= len(board) or point[1] >= len(board[0])

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

#                               #
#       FINDING POSITIONS       #
#                               #

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
            if isOutOfBounds(board, point) or board[point[0]][point[1]].isInactive():
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

#                               #
#    UTILITIES FOR POSITIONS    #
#                               #

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
    pass # STUB: maybe implemented later?