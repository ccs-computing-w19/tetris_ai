from drawing.color import *
from enum import Enum
from tetris.tetris import Tile

class Drawing():

    # DEFINE COLOR CONSTANTS:
    BORDERCOLOR = (10, 10, 80)
    BGCOLOR = (50, 50, 175)
    TEXTCOLOR = (255, 255, 255)
    TEXTSHADOWCOLOR = (180, 170, 170)
    BLANKCOLOR = (212, 226, 238)
    LIGHTBLANKCOLOR = (222, 236, 248)
    CANVASCOLOR = (180, 170, 170)
    BUTTONCOLOR = (100, 100, 200)

    def __init__(self, pygame, displaySurf, width, height):
        self.pygame = pygame
        self.DISPLAYSURF = displaySurf
        self.WINDOWWIDTH, self.WINDOWHEIGHT = width, height

    def fill(self):
        self.DISPLAYSURF.fill(self.BGCOLOR)
    
    def drawText(self, text, font, location, color=None, center=False):
        textSurf = font.render(text, True, color if color else self.TEXTCOLOR)
        textRect = textSurf.get_rect()
        if center: textRect.center = location
        else: textRect.topleft = location
        self.DISPLAYSURF.blit(textSurf, textRect)

    def drawStatus(self, score, level, piece, font, location):
        #pygame.draw.rect(DISPLAYSURF, BGCOLOR, pygame.Rect(location + (100, 100)))
        self.drawText("Score: %s" % score, font, location)
        self.drawText("Level: %s" % level, font, (location[0], location[1] + 30))
        self.drawText("Piece: %s" % piece, font, (location[0], location[1] + 60))

    def drawBoard(self, board, numColors, location, bordersize, boxsize):
        # draw the border and box
        self.pygame.draw.rect(self.DISPLAYSURF, self.BORDERCOLOR, (location[0], location[1], (len(board[0]) * boxsize + bordersize), (len(board) * boxsize + bordersize)), bordersize)
        self.pygame.draw.rect(self.DISPLAYSURF, self.CANVASCOLOR, (location[0] + bordersize // 2, location[1] + bordersize // 2, boxsize * len(board[0]), boxsize * len(board)))

        # draw the individual boxes on the board
        for y in range(len(board)):
            for x in range(len(board[y])):
                pixelx = location[0] + bordersize // 2 + (x * boxsize)
                pixely = location[1] + bordersize // 2 + (y * boxsize)
                self.pygame.draw.rect(self.DISPLAYSURF, getColorFromNumber(board[y][x].color, numColors) if board[y][x].color != 0 else self.LIGHTBLANKCOLOR, (pixelx + 1, pixely + 1, boxsize - 1, boxsize - 1))
                self.pygame.draw.rect(self.DISPLAYSURF, getLightFromNumber(board[y][x].color, numColors) if board[y][x].color != 0 else self.LIGHTBLANKCOLOR, (pixelx + 1, pixely + 1, boxsize - 4, boxsize - 4))

    def drawNextPiece(self, piece, numColors, font, color, location, bordersize, boxsize):
        DIMENSIONS = (4, 4)
        #pygame.draw.rect(DISPLAYSURF, BGCOLOR, pygame.Rect(location + (100, 100)))
        self.drawText("Next: ", font, location)
        
        # draw 'little board'
        grid = [[Tile() for j in range(DIMENSIONS[0])] for i in range(DIMENSIONS[1])]
        for loc in piece:
            grid[loc[0] + 1][loc[1]] = Tile(state=2, pivot=loc[2], color=color) # 1 is the vertical offset
        self.drawBoard(grid, numColors, (location[0], location[1] + 25), bordersize, boxsize)

    def drawMenu(self, text, font1, font2):
        self.drawText(text, font1, (int(self.WINDOWWIDTH / 2), int(self.WINDOWHEIGHT / 2) - 30), color=self.TEXTSHADOWCOLOR, center=True)
        self.drawText(text, font1, (int(self.WINDOWWIDTH / 2) - 3, int(self.WINDOWHEIGHT / 2) - 30 - 3), center=True)
        
        # Draw the additional "Press a key to play." text.
        self.drawText("Press a key to play.", font2, (int(self.WINDOWWIDTH / 2), int(self.WINDOWHEIGHT / 2) + 30), center=True)


