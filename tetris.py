from random import choice, randint
import time, os, curses, copy

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

class Board:

    def __init__(self):
        self.grid = [[Tile() for j in range(10)] for i in range(20)]
        self.turns = 0
        self.lost = False
        self.lineClears = 0
        self.next = randint(1, len(self.PIECES))
        self.autoChoice = True
        self.pivot = (-1, -1) #flag that stores the pivot
        self.generateNewPiece()

    def getBoard(self):
        return copy.deepcopy(self.grid)
        
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
    ]

    def generateNewPiece(self):
        for loc in self.PIECES[self.next - 1]:
            self.grid[loc[0]][loc[1]] = Tile(state=2, pivot=loc[2])
            if loc[2]: self.pivot = (loc[0], loc[1])
        if self.autoChoice:
            self.next = randint(1, len(self.PIECES))

    def rotateActiveClockwise(self):
        if self.rotatable(): #if there is a pivot
            error = False
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j].isActive():
                        if self.pivot[0] + j - self.pivot[1] > 19 or self.pivot[1] + self.pivot[0] - i > 9 or self.pivot[0] + j - self.pivot[1] < 0 or self.pivot[1] + self.pivot[0] - i < 0 or self.grid[self.pivot[0] + j - self.pivot[1]][self.pivot[1] + self.pivot[0] - i].isInactive():
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

    def translateActiveRight(self):
        onRight = False
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j].isActive():
                    if j == 9 or self.grid[i][j+1].isInactive(): onRight = True; break
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

    def incrementTime(self):
        onBottom = False
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j].isActive():
                    if i == 19 or self.grid[i+1][j].isInactive(): onBottom = True; break
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
        self.turns += 1
        self.updateBoard()
        if onBottom:
            for i in range(len(self.grid[0])):
                if self.grid[0][i].isInactive(): self.lost = True; break
            self.pivot = (-1, -1)
            self.lineClear()
            self.generateNewPiece()
    
    def lineClear(self):
        for i in range(len(self.grid)):
            rowIsFull = True
            for j in range(len(self.grid[i])):
                if not self.grid[i][j].isInactive(): rowIsFull = False #break
            if rowIsFull:
                for r in range(i, 0, -1):
                    self.grid[r] = self.grid[r-1]
                self.grid[0] = [Tile() for j in range(10)]
                self.lineClears += 1

    def display(self, window):
        window.clear()
        window.addstr("\n |--------------------|\n")
        for row in self.grid:
            window.addstr(" |")
            for tile in row:
                window.addstr("[]" if tile.state else "  ")
            window.addstr("|\n")
        window.addstr(" |--------------------|\n")
        window.addstr("\n  " + "".join([("[]" if (-1, i, False) in self.PIECES[self.next-1] or (-1, i, True) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " turns: " + str(self.turns))
        window.addstr("\n  " + "".join([("[]" if (0, i, False) in self.PIECES[self.next-1] or (0, i, True) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " lost: " + str(self.lost))
        window.addstr("\n  " + "".join([("[]" if (1, i, False) in self.PIECES[self.next-1] or (1, i, True) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " clears: " + str(self.lineClears))
        window.addstr("\n  " + "".join([("[]" if (2, i, False) in self.PIECES[self.next-1] or (2, i, True) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " next: " + str(self.next))
        window.addstr("{}".format(self.pivot))
        window.addstr("\n")



def main(win):
    curses.noecho() #stop keys echoing to screen
    win.nodelay(True)
    
    # Load screen:
    try:
        win.addstr(" ______________________\n")
        for i in range(10):
            win.addstr(" \n")
        win.addstr("         TETRIS        \n")
        win.addstr("    by Ben and Daniel  \n")
        win.addstr("      press any key    \n")
        for i in range(14):
            win.addstr(" \n")
        win.addstr(" ______________________\n")
    except Exception as e:
        raise Exception('Window too small; (29x24 required)') # Don't! If you catch, likely to hide bugs. 
    while 1:
        try:
            key = win.getkey()
            if key == os.linesep or key == 'q':
                quit()
            else: #if any other key was pressed
                break
        except Exception as e:
            # No input
            pass

    # Play screen:
    board = Board()
    board.display(win)
    counter = int(time.time())
    while 1:
        try:
            key = win.getkey()
            if key == 'q':
                quit()
            if key == 's' or key == 'KEY_DOWN':
                board.incrementTime()
                board.display(win)
            if key == 'a' or key == 'KEY_LEFT':
                board.translateActiveLeft()
                board.display(win)
            if key == 'd' or key == 'KEY_RIGHT':
                board.translateActiveRight()
                board.display(win)
            if key == 'w' or key == 'KEY_UP':
                board.rotateActiveClockwise()
                board.display(win)
            if key in ['{}'.format(i) for i in range(8)]:
                if key == '0':
                    board.autoChoice = True
                    board.next = randint(1, 7)
                else:
                    board.autoChoice = False
                    board.next = int(key)
                board.display(win)
        except Exception as e:
            # No input
            current = int(time.time())
            if counter < current:
                board.incrementTime()
                board.display(win)
                counter = current

if __name__ == '__main__':
    curses.wrapper(main)
