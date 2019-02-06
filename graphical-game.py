#!/usr/bin/env python3

import tetris
import pygame, sys
from math import pi, sin

FPS = 30
WINDOWWIDTH = 580
WINDOWHEIGHT = 700
BOXSIZE = 30
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = (WINDOWWIDTH - BOARDWIDTH * BOXSIZE) // 2
TOPMARGIN = (WINDOWHEIGHT - BOARDHEIGHT * BOXSIZE) // 2 - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (192, 192, 192)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
DARKBLUE    = (  0,   0,  50)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)
LIGHTYELLOW = (175, 175,  20)
BOTTILIGHT  = (222, 236, 248)
BOTTICELLI  = (212, 226, 238)

BORDERCOLOR = DARKBLUE
BGCOLOR = LIGHTBLUE
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
BLANKCOLOR = BOTTICELLI
LIGHTBLANKCOLOR = BOTTILIGHT
CANVASCOLOR = GRAY

# Code to generate block colors
MAXCOLORS = 360
def getColorFromNumber(n):
    red = int(min(max(100 * (sin((n + 90) * pi / 180) + 1), 44), 162))
    green = int(min(max(100 * (sin((n + 210) * pi / 180) + 1), 44), 162))
    blue = int(min(max(100 * (sin((n + 330) * pi / 180) + 1), 44), 162))
    return (red, green, blue)

def getLightFromNumber(n):
    red = int(min(max(125 * (sin((n + 90) * pi / 180) + 1), 55), 204))
    green = int(min(max(125 * (sin((n + 210) * pi / 180) + 1), 55), 204))
    blue = int(min(max(125 * (sin((n + 330) * pi / 180) + 1), 55), 204))
    return (red, green, blue)

def start():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Enomino')

    ### Start menu:
    showTextScreen('Enomino')
    ready = False
    while not ready: # start screen loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                terminate() # exit game
            if event.type == pygame.KEYDOWN:
                ready = True
        pygame.display.update()
        FPSCLOCK.tick()


def main():
    game = tetris.Tetris(numColors=MAXCOLORS)

    drawStatus(game.numTurns, game.numLines, game.next)
    drawBoard(game.getBoard())
    elapsed = 0
    speed = 30 # higher is slower
    while not game.lost: # game loop ends when game is lost
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT:
                terminate() # exit game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotateActiveClockwise()
                if event.key == pygame.K_DOWN:
                    game.incrementTime()
                    elapsed = 0
                if event.key == pygame.K_RIGHT:
                    game.translateActiveRight()
                if event.key == pygame.K_LEFT:
                    game.translateActiveLeft()
                if event.key == pygame.K_SPACE:
                    game.hardDrop()
                drawBoard(game.getBoard())
        
        if elapsed > speed:
            game.incrementTime()
            elapsed = 0
            drawStatus(game.numTurns, game.numLines, game.next)
            drawBoard(game.getBoard())

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        elapsed += 1

    ### End menu:
    showTextScreen('Game Over')
    ready = False
    while not ready: # start screen loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate() # exit game
            if event.type == pygame.KEYDOWN:
                ready = True
        pygame.display.update()
        FPSCLOCK.tick()


def terminate():
    pygame.quit()
    sys.exit()


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def showTextScreen(text):
    DISPLAYSURF.fill(BGCOLOR)

    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    if color != 100:
        pygame.draw.rect(DISPLAYSURF, getColorFromNumber(color) if color != 0 else LIGHTBLANKCOLOR, (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
        pygame.draw.rect(DISPLAYSURF, getLightFromNumber(color) if color != 0 else LIGHTBLANKCOLOR, (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    DISPLAYSURF.fill(BGCOLOR)

    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 3, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, CANVASCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for y in range(len(board)):
        for x in range(len(board[y])):
            drawBox(x, y, board[y][x].color)


def drawStatus(score, level, piece):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

    # draw the next piece indicator
    pieceSurf = BASICFONT.render('Piece: %s' % piece, True, TEXTCOLOR)
    pieceRect = levelSurf.get_rect()
    pieceRect.topleft = (WINDOWWIDTH - 150, 80)
    DISPLAYSURF.blit(pieceSurf, pieceRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 110)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=130)




if __name__ == "__main__":
    start()
    while True:
        main()
