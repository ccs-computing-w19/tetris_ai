import tetris, copy

def print_out(board):
    for i in range(len(board)):
        string = ""
        for j in range(len(board[i])):
            string += str(board[i][j].state)
        print(string)

def rotate(point, pivot):
    return (point[1] - pivot[1] + pivot[0], pivot[0] - point[0] + pivot[1], point[2] + 1)

# return: list of end positions, parameter: game board
def findPositions(board, rotatable):
    print_out(board)
    tiles = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].state == 2: tiles.append((i, j))
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
    # prune options:
    pruned = []
    for arrangement in arrangements:
        valid = True
        for point in arrangement:
            if point[0] < 0 or point[0] >= len(board) or point[1] < 0 or point[1] >= len(board[0]) or board[point[0]][point[1]].isInactive():
                valid = False; break
        if valid:
            for point in arrangement:
                if point[0] == len(board) - 1 or board[point[0] + 1][point[1]].isInactive():
                    pruned.append(arrangement); break
    print(pruned)

    #while a < len(arrangements):
    #   onBottom = False
    #    for point in arrangements[a]:
    #        if point[0] < 0 or point[0] >= len(board) or point[1] < 0 or point[1] >= len(board[0]) or board[point[0]][point[1]].isInactive():
    #            del arrangements[a]; break
    #        elif point[0] == len(board) - 1 or board[point[0] + 1][point[1]].isInactive():
    #            onBottom = True
    #    if not onBottom:
    #        print('A:', len(arrangements))
    #        del arrangements[a]
    #        print('B:', len(arrangements))
    #    a += 1
    #print(arrangements)

# return: series of moves, parameter: end position, game board
def findPath(board):
    pass
