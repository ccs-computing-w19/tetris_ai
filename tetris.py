from random import choice, randint
import time, os, curses, copy

class Tile:

    def __init__(self, state=0, color=0, pivot=False):
        self.state = state #state of the tile: 0 is inactive, 1 is inactive, 2 is active
        self.color = 0 #value from 0 to 5
        self.pivot = False #pieces should rotate around pivot
        self.updated = False
        self.resetNext()

    def copy(self, tile):
        self.nextState = tile.state
        self.nextColor = tile.color
        self.nextPivot = tile.pivot
        self.updated = True
    
    def update(self):
        self.state = self.nextState
        self.color = self.nextColor
        self.pivot = self.nextPivot
        self.resetNext()

    def reset(self):
        self.state = 0
        self.color = 0
        self.pivot = False
        self.resetNext()
    
    def resetNext(self):
        self.nextState = self.state
        self.nextColor = self.color
        self.nextPivot = self.pivot
        self.updated = False
    
    def isActive(self):
        return self.state == 2

    def isEmpty(self):
        return self.state == 0

class Board:

    PIECES = [
        [(0, 3, 1), (0, 4, 5), (0, 5, 1), (0, 6, 1)],
        [(0, 3, 1), (0, 4, 5), (0, 5, 1), (1, 4, 1)],
        [(0, 4, 1), (0, 5, 5), (0, 6, 1), (1, 4, 1)],
        [(0, 3, 1), (0, 4, 5), (0, 5, 1), (1, 5, 1)],
        [(0, 4, 1), (0, 5, 1), (1, 4, 1), (1, 5, 1)],
        [(0, 3, 1), (0, 4, 1), (1, 4, 5), (1, 5, 1)],
        [(0, 5, 1), (0, 6, 1), (1, 4, 1), (1, 5, 5)],
    ]

    def __init__(self):
        self.grid = [[Tile() for j in range(10)] for i in range(20)]
        self.turns = 0
        self.lost = False
        self.lineClears = 0
        self.next = randint(1, 7)
        self.autoChoice = True
        self.rotatable = False #flag that stores if rotate button does anything
        self.generateNewPiece()

    def getBoard(self):
        return copy.deepcopy(self.grid)
        
    def display(self, window):
        window.clear()
        window.addstr("\n |--------------------|\n")
        for row in self.grid:
            window.addstr(" |")
            for tile in row:
                #self.window.addstr("{} ".format(i))
                window.addstr("{}".format("  " if tile.state == 0 else "[]"))
            window.addstr("|\n")
        window.addstr(" |--------------------|\n")
        window.addstr("\n  " + "".join([("[]" if (-1, i, 1) in self.PIECES[self.next-1] or (-1, i, 5) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " turns: " + str(self.turns))
        window.addstr("\n  " + "".join([("[]" if (0, i, 1) in self.PIECES[self.next-1] or (0, i, 5) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " lost: " + str(self.lost))
        window.addstr("\n  " + "".join([("[]" if (1, i, 1) in self.PIECES[self.next-1] or (1, i, 5) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " clears: " + str(self.lineClears))
        window.addstr("\n  " + "".join([("[]" if (2, i, 1) in self.PIECES[self.next-1] or (2, i, 5) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " next: " + str(self.next))
        window.addstr("\n")

    def generateNewPiece(self):
        for loc in self.PIECES[self.next - 1]:
            self.grid[loc[0]][loc[1]].state = loc[2]
        if self.autoChoice:
            self.next = randint(1, 7)

    def rotateActiveClockwise(self):
        pivot = (-1, -1)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 5:
                    pivot = (i, j) #break
        if pivot[0] != -1:
            error = False
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == 1 or self.grid[i][j] == 4:
                        if pivot[0] + j - pivot[1] > 19 or pivot[1] + pivot[0] - i > 9 or pivot[0] + j - pivot[1] < 0 or pivot[1] + pivot[0] - i < 0 or self.grid[pivot[0] + j - pivot[1]][pivot[1] + pivot[0] - i] == 2:
                            error = True #break
            if not error:
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        if self.grid[i][j] == 1 or self.grid[i][j] == 4:
                            self.grid[pivot[0] + j - pivot[1]][pivot[1] + pivot[0] - i] += 3
                            self.grid[i][j] -= 1
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        if self.grid[i][j] == 3 or self.grid[i][j] == 4:
                            self.grid[i][j] -= 2
    
    # MAKE THIS FUNCTION WORK
    def rotateActiveCounter(self):
        pivot = (-1, -1)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 5:
                    pivot = (i, j) #break
        if pivot[0] != -1:
            error = False
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == 1 or self.grid[i][j] == 4:
                        if pivot[0] + j - pivot[1] > 19 or pivot[1] + pivot[0] - i > 9 or pivot[0] + j - pivot[1] < 0 or pivot[1] + pivot[0] - i < 0 or self.grid[pivot[0] + j - pivot[1]][pivot[1] + pivot[0] - i] == 2:
                            error = True #break
            if not error:
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        if self.grid[i][j] == 1 or self.grid[i][j] == 4:
                            self.grid[pivot[0] + j - pivot[1]][pivot[1] + pivot[0] - i] += 3
                            self.grid[i][j] -= 1
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        if self.grid[i][j] == 3 or self.grid[i][j] == 4:
                            self.grid[i][j] -= 2

    def translateActiveLeft(self):
        onLeft = False
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1 or self.grid[i][j] == 5:
                    if j == 0 or self.grid[i][j-1] == 2:
                        onLeft = True #break
        if not onLeft:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == 1 or self.grid[i][j] == 5:
                        self.grid[i][j-1] = self.grid[i][j]
                        self.grid[i][j] = 0

    def translateActiveRight(self):
        onRight = False
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1 or self.grid[i][j] == 5:
                    if j == 9 or self.grid[i][j+1] == 2:
                        onRight = True #break
        if not onRight:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])-1, -1, -1):
                    if self.grid[i][j] == 1 or self.grid[i][j] == 5:
                        self.grid[i][j+1] = self.grid[i][j]
                        self.grid[i][j] = 0

    def incrementTime(self):
        onBottom = False
        noneActive = True
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j].state == 2:
                    noneActive = False
                    if i == 19 or self.grid[i+1][j].state == 1:
                        onBottom = True
        if noneActive:
            self.generateNewPiece()
        elif onBottom:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j].state == 2:
                        self.grid[i][j].nextState = 1
            #self.lineClear()
            #if 2 in self.grid[0]: self.lost = True
            self.generateNewPiece()
        else:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j].isActive:
                        self.grid[i+1][j].copy(self.grid[i][j])
        self.turns += 1
        self.updateBoard()

    def lineClear(self):
        for i in range(len(self.grid)):
            if not (0 in self.grid[i]):
                for j in range(i, 0, -1):
                    self.grid[j] = self.grid[j-1]
                self.grid[0] = [0 for j in range(10)]
                self.lineClears += 1

    def updateBoard(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j].update()

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
            if key == os.linesep or key == 'q':
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
                #board.incrementTime()
                board.display(win)
                counter = current

if __name__ == '__main__':
    curses.wrapper(main)
