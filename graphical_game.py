#!/usr/bin/env python3

import tetris
import pygame, sys
from math import pi, sin
import random

FPS = 30
WINDOWWIDTH = 480
WINDOWHEIGHT = 600

# DEFINE COLOR CONSTANTS:
MAXCOLORS = 360
BORDERCOLOR = (10, 10, 80)
BGCOLOR = (50, 50, 175)
TEXTCOLOR = (255, 255, 255)
TEXTSHADOWCOLOR = (180, 170, 170)
BLANKCOLOR = (212, 226, 238)
LIGHTBLANKCOLOR = (222, 236, 248)
CANVASCOLOR = (180, 170, 170)


INPUT = False
DELAY = 1 # delay between each incrementTime
    


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 72)
    pygame.display.set_caption('Enomino')

    playStartMenu()
    while True:
        playGame()
        playEndMenu()


def playStartMenu():
    DISPLAYSURF.fill(BGCOLOR)

    text = "Enomino"
    # Draw the text drop shadow
    drawText(text, BIGFONT, TEXTSHADOWCOLOR, (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 30), True)

    # Draw the text
    drawText(text, BIGFONT, TEXTCOLOR, (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 30 - 3), True)

    # Draw the additional "Press a key to play." text.
    drawText("Press a key to play.", BASICFONT, TEXTCOLOR, (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 30), True)

    ready = False
    while not ready: # start screen loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                terminate() # exit game
            if event.type == pygame.KEYDOWN:
                ready = True
        pygame.display.update()
        FPSCLOCK.tick()


def playGame():
    game = tetris.Tetris(numColors=MAXCOLORS)
    render(game)

    # loop count variables:
    numTicks = 0
    timeSinceIncrement = 0

    # set up ai:
    moves = []
    numPieces = 0

    pressedKeys = [-1, -1, -1, -1] # up, down, left, right
    while not game.lost: # game loop ends when game is lost

        if INPUT: handleInput(game, pressedKeys, numTicks)
        else:
            for event in pygame.event.get(): # event handling loop
                if event.type == pygame.QUIT:
                    terminate() # exit game
        
        # increment time (move blocks down)
        if timeSinceIncrement > DELAY: # number of ticks between time increments
            
            if not INPUT: moves, numPieces = ai(game, moves, numPieces)
            
            game.incrementTime()
            timeSinceIncrement = 0
            render(game)

        FPSCLOCK.tick(FPS)
        numTicks += 1
        timeSinceIncrement += 1



def ai(game, moves, numPieces):
    if game.numPieces > numPieces:
        n = random.randint(-5, 5)
        for i in range(random.randint(0, 3)):
            game.rotateActiveClockwise()
        if n > 0:
            for i in range(n):
                game.translateActiveLeft()
        else:
            for i in range(-n):
                game.translateActiveRight()
        numPieces += 1
    return moves, numPieces


def handleInput(game, pressedKeys, numTicks):
    for event in pygame.event.get(): # event handling loop
        if event.type == pygame.QUIT:
            terminate() # exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotateActiveClockwise()
                pressedKeys[0] = 0
            if event.key == pygame.K_DOWN:
                game.incrementTime()
                pressedKeys[1] = 0
                timeSinceIncrement = 0
            if event.key == pygame.K_LEFT:
                game.translateActiveLeft()
                pressedKeys[2] = 0
            if event.key == pygame.K_RIGHT:
                game.translateActiveRight()
                pressedKeys[3] = 0
            if event.key == pygame.K_SPACE:
                game.hardDrop()
                timeSinceIncrement = 0
            if event.key == pygame.K_z:
                game.rotateActiveCounterclockwise()
            
            if event.key == pygame.K_0: game.setNextPiece(0)
            if event.key == pygame.K_1: game.setNextPiece(1)
            if event.key == pygame.K_2: game.setNextPiece(2)
            if event.key == pygame.K_3: game.setNextPiece(3)
            if event.key == pygame.K_4: game.setNextPiece(4)
            if event.key == pygame.K_5: game.setNextPiece(5)
            if event.key == pygame.K_6: game.setNextPiece(6)
            if event.key == pygame.K_7: game.setNextPiece(7)
            if event.key == pygame.K_8: game.setNextPiece(8)
            if event.key == pygame.K_9: game.setNextPiece(9)
            if event.key == pygame.K_q: game.setNextPiece(10)
            if event.key == pygame.K_w: game.setNextPiece(11)

            render(game)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                pressedKeys[0] = -1
            if event.key == pygame.K_DOWN:
                pressedKeys[1] = -1
            if event.key == pygame.K_LEFT:
                pressedKeys[2] = -1
            if event.key == pygame.K_RIGHT:
                pressedKeys[3] = -1

    # deal with held-down keys:
    THRESHOLD = 5 # in ticks
    for i in range(len(pressedKeys)):
        pressedKeys[i] += 1 if pressedKeys[i] != -1 else 0
    if pressedKeys[0] > 10 and numTicks % 2: # only every other tick
        game.rotateActiveClockwise()
        render(game)
    if pressedKeys[1] > 10 and numTicks % 2:
        game.incrementTime()
        render(game)
        timeSinceIncrement = 0
    if pressedKeys[2] > 10 and numTicks % 2:
        game.translateActiveLeft()
        render(game)
    if pressedKeys[3] > 10 and numTicks % 2:
        game.translateActiveRight()
        render(game)


def playEndMenu():
    DISPLAYSURF.fill(BGCOLOR)

    text = "Game Over"
    # Draw the text drop shadow
    drawText(text, BIGFONT, TEXTSHADOWCOLOR, (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 30), True)

    # Draw the text
    drawText(text, BIGFONT, TEXTCOLOR, (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 30 - 3), True)

    # Draw the additional "Press a key to play." text.
    drawText("Press a key to play.", BASICFONT, TEXTCOLOR, (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 30), True)

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


def drawText(text, font, color, location, center=False):
    textSurf = font.render(text, True, color)
    textRect = textSurf.get_rect()
    if center:
        textRect.center = location
    else:
        textRect.topleft = location
    DISPLAYSURF.blit(textSurf, textRect)


def drawStatus(score, level, piece, location):
    # draw the score text
    drawText("Score: %s" % score, BASICFONT, TEXTCOLOR, location)

    # draw the level text
    drawText("Level: %s" % level, BASICFONT, TEXTCOLOR, (location[0], location[1] + 30))

    # draw the next piece indicator
    drawText("Piece: %s" % piece, BASICFONT, TEXTCOLOR, (location[0], location[1] + 60))


# Code to generate block shadows
def getColorFromNumber(n):
    red = int(min(max(100 * (sin((n + MAXCOLORS * (90 / 360)) * pi / 180) + 1), 44), 162))
    green = int(min(max(100 * (sin((n + MAXCOLORS * (210 / 360)) * pi / 180) + 1), 44), 162))
    blue = int(min(max(100 * (sin((n + MAXCOLORS * (330 / 360)) * pi / 180) + 1), 44), 162))
    return (red, green, blue)

# Code to generate block colors
def getLightFromNumber(n):
    red = int(min(max(125 * (sin((n + MAXCOLORS * (90 / 360)) * pi / 180) + 1), 55), 204))
    green = int(min(max(125 * (sin((n + MAXCOLORS * (210 / 360)) * pi / 180) + 1), 55), 204))
    blue = int(min(max(125 * (sin((n + MAXCOLORS * (330 / 360)) * pi / 180) + 1), 55), 204))
    return (red, green, blue)


def drawBoard(board, location):
    BORDER = 5 # border size
    BOXSIZE = 25 # size of tiles

    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (location[0], location[1], (len(board[0]) * BOXSIZE + BORDER), (len(board) * BOXSIZE + BORDER)), BORDER)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, CANVASCOLOR, (location[0] + BORDER // 2, location[1] + BORDER // 2, BOXSIZE * len(board[0]), BOXSIZE * len(board)))

    # draw the individual boxes on the board
    for y in range(len(board)):
        for x in range(len(board[y])):
            pixelx = location[0] + BORDER // 2 + (x * BOXSIZE)
            pixely = location[1] + BORDER // 2 + (y * BOXSIZE)
            pygame.draw.rect(DISPLAYSURF, getColorFromNumber(board[y][x].color) if board[y][x].color != 0 else LIGHTBLANKCOLOR, (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
            pygame.draw.rect(DISPLAYSURF, getLightFromNumber(board[y][x].color) if board[y][x].color != 0 else LIGHTBLANKCOLOR, (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawNextPiece(piece, color, location):
    DIMENSIONS = (4, 4)

    # draw "next:" text
    drawText("Next: ", BASICFONT, TEXTCOLOR, location)

    # build grid structure
    grid = [[tetris.Tile() for j in range(DIMENSIONS[0])] for i in range(DIMENSIONS[1])]
    for loc in piece:
        grid[loc[0] + 1][loc[1]] = tetris.Tile(state=2, pivot=loc[2], color=color) # 1 is the vertical offset
    
    # draw "board"
    drawBoard(grid, (location[0], location[1] + 25))


def render(game):
    DISPLAYSURF.fill(BGCOLOR)
    drawBoard(game.getBoard(), (50, 50))
    drawNextPiece(game.PIECES[game.next - 1], game.nextColor, (WINDOWWIDTH - 150, 150))
    drawStatus(game.numTurns, game.numLines, game.next, (WINDOWWIDTH - 150, 50))
    pygame.display.update()




if __name__ == "__main__":
    main()

