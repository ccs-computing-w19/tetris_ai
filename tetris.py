from random import choice, randint
import copy

class Tile:

    def __init__(self, state=0, color=0, pivot=False):
        self.state = state #state of the tile: 0 is inactive, 1 is inactive, 2 is active
        self.color = color #value from 0 to 5
        self.pivot = pivot #pieces should rotate around pivot
        self.nextState = self.state
        self.nextColor = self.color
        self.nextPivot = self.pivot
        self.updated = False

    def copy(self, tile):
        self.nextState = tile.state
        self.nextColor = tile.color
        self.nextPivot = tile.pivot
        self.updated = True
    
    def update(self):
        self.state = self.nextState
        self.color = self.nextColor
        self.pivot = self.nextPivot
        self.updated = False

    def reset(self):
        self.nextState = 0
        self.nextColor = 0
        self.nextPivot = False
        self.updated = True
    
    def deactivate(self):
        if self.isActive:
            self.nextState = 1
            self.nextPivot = False
        self.updated = True
    
    def isActive(self):
        return self.state == 2

    def isInactive(self):
        return self.state == 1

    def isEmpty(self):
        return self.state == 0

class Tetris:

    def __init__(self, numRows=20, numColumns=10, numColors=0):
        self.grid = [[Tile() for j in range(numColumns)] for i in range(numRows)]
        self.numColors = numColors

        self.next = self.randomPiece()
        self.nextColor = self.randomColor()
        self.autoChoice = True
        self.pivot = (-1, -1) #flag that stores the pivot

        self.lost = False
        self.numTurns = 0
        self.numLines = 0
        self.numPieces = 0

        self.generateNewPiece()
    
    def rotatable(self):
        return self.pivot != (-1, -1)

    def updateBoard(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j].updated: self.grid[i][j].update()
    
    PIECES = [
        [(0, 3, False), (0, 4, True), (0, 5, False), (0, 6, False)],
        [(0, 3, False), (0, 4, True), (0, 5, False), (1, 4, False)],
        [(0, 4, False), (0, 5, True), (0, 6, False), (1, 4, False)],
        [(0, 3, False), (0, 4, True), (0, 5, False), (1, 5, False)],
        [(0, 4, False), (0, 5, False), (1, 4, False), (1, 5, False)],
        [(0, 3, False), (0, 4, False), (1, 4, True), (1, 5, False)],
        [(0, 5, False), (0, 6, False), (1, 4, False), (1, 5, True)],
        #EXTRA:
        [(0, 3, False), (0, 4, True), (1, 4, False)],
        [(0, 3, False), (0, 4, True), (0, 5, False)],
        [(0, 4, False), (0, 5, True)],
        [(0, 4, False)],
    ]

    def randomPiece(self):
        return randint(1, len(self.PIECES))

    def randomColor(self):
        return randint(1, self.numColors)

    # Creates a new piece at the top of the board
    def generateNewPiece(self):
        for loc in self.PIECES[self.next - 1]: # subtract 1 for zero-indexing
            self.grid[loc[0]][loc[1]] = Tile(state=2, pivot=loc[2], color=self.nextColor)
            if loc[2]: self.pivot = (loc[0], loc[1])
        if self.autoChoice:
            self.next = self.randomPiece()
        self.nextColor = self.randomColor()
        self.numPieces += 1

    # Rotates the active block clockwise
    def rotateActiveClockwise(self):
        if self.rotatable(): #if there is a pivot
            error = False
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j].isActive():
                        if self.pivot[0] + j - self.pivot[1] > len(self.grid) - 1 or self.pivot[1] + self.pivot[0] - i > len(self.grid[0]) - 1 or self.pivot[0] + j - self.pivot[1] < 0 or self.pivot[1] + self.pivot[0] - i < 0 or self.grid[self.pivot[0] + j - self.pivot[1]][self.pivot[1] + self.pivot[0] - i].isInactive():
                            error = True; break
                else:
                    continue
                break
            if not error:
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        if self.grid[i][j].isActive():
                            self.grid[self.pivot[0] + j - self.pivot[1]][self.pivot[1] + self.pivot[0] - i].copy(self.grid[i][j])
                            if not self.grid[i][j].updated: self.grid[i][j].reset()
                self.updateBoard()
    
    # Rotates the active block clockwise
    def rotateActiveCounterclockwise(self):
        pass
    
    # Moves the active block left
    def translateActiveLeft(self):
        onLeft = False
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j].isActive():
                    if j == 0 or self.grid[i][j-1].isInactive(): onLeft = True; break
            else:
                continue
            break
        if not onLeft:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j].isActive():
                        self.grid[i][j-1].copy(self.grid[i][j])
                        if not self.grid[i][j].updated: self.grid[i][j].reset()
            if self.rotatable(): self.pivot = (self.pivot[0], self.pivot[1] - 1) #update pivot flag
            self.updateBoard()

    # Moves the active block right
    def translateActiveRight(self):
        onRight = False
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j].isActive():
                    if j == len(self.grid[0]) - 1 or self.grid[i][j+1].isInactive(): onRight = True; break
            else:
                continue
            break
        if not onRight:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j].isActive():
                        self.grid[i][j+1].copy(self.grid[i][j])
                        if not self.grid[i][j].updated: self.grid[i][j].reset()
            if self.rotatable(): self.pivot = (self.pivot[0], self.pivot[1] + 1) #update pivot flag
            self.updateBoard()

    # Shifts blocks down and generates new block if necessary
    def incrementTime(self):
        onBottom = False
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j].isActive():
                    if i == len(self.grid) - 1 or self.grid[i+1][j].isInactive(): onBottom = True; break
            else:
                continue
            break
        if onBottom:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j].isActive():
                        self.grid[i][j].deactivate()
        else:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j].isActive():
                        self.grid[i+1][j].copy(self.grid[i][j])
                        if not self.grid[i][j].updated: self.grid[i][j].reset()
            if self.rotatable(): self.pivot = (self.pivot[0] + 1, self.pivot[1]) #update pivot flag
        self.numTurns += 1
        self.updateBoard()
        if onBottom:
            for i in range(len(self.grid[0])):
                if self.grid[0][i].isInactive(): self.lost = True; break
            self.pivot = (-1, -1)
            self.lineClear()
            self.generateNewPiece()
    
    # Drops the active piece to the bottom
    def hardDrop(self):
        currentPieces = self.numPieces
        while currentPieces == self.numPieces:
            self.incrementTime()

    # Clears any lines that are full
    def lineClear(self):
        for i in range(len(self.grid)):
            rowIsFull = True
            for j in range(len(self.grid[i])):
                if not self.grid[i][j].isInactive(): rowIsFull = False; break
            if rowIsFull:
                for r in range(i, 0, -1):
                    self.grid[r] = self.grid[r-1]
                self.grid[0] = [Tile() for j in range(len(self.grid[0]))]
                self.numLines += 1

    def getBoard(self):
        return copy.copy(self.grid)

