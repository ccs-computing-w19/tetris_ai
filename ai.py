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
    return (point[1] - pivot[1] + pivot[0], pivot[0] - point[0] + pivot[1], point[2] + 1)

# return: position of active piece
# params: game board
def getActivePosition(board):
    position = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].state == 2: position.append((i, j, 0))
            # position[2] is the rotation, which is default, so 0
    return position

# return: list of valid end positions
# params: game board, if the piece is rotatable
def findPositions(board, rotatable):
    # find the position of the initial piece:
    tiles = getActivePosition(board)
    # then, find every translation and rotation of the initial position:
    arrangements = []
    for i in range(-tiles[0][0], -tiles[0][0] + len(board)):
        for j in range(-tiles[0][1], -tiles[0][1] + len(board[i])):
            # rotation is communitive, any pivot can be used
            arrangement = []
            for k in range(len(tiles)):
                point = (i + tiles[k][0], j + tiles[k][1], 0)
                arrangement.append(point)
            arrangements.append(arrangement)
            if rotatable:
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

# return: series of moves ['d', 'd', 'r', 'r', 'r', 'l', 'l', 'l', 'd']
# params: game board, final position of piece
def findPath(board, position):
    start = getActivePosition(board)

