#!/usr/bin/env python3

from tetris.tetris import Tetris, Tile
import pygame, sys, random, time
from math import pi, sin

FPS = 60
WINDOWWIDTH = 960
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
BUTTONCOLOR = (100, 100, 200)

DELAY = 20 # delay between each incrementTime

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
        response = playGame()
        playEndMenu(response)


def playStartMenu():
    DISPLAYSURF.fill(BGCOLOR)
    
    text = "Enomino"
    drawText(text, BIGFONT, TEXTSHADOWCOLOR, (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 30), True)
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

from ai.ai import AI
def playGame():
    seed = int(time.time())
    game = Tetris(numColors=MAXCOLORS, seed=seed)
    aiGame = Tetris(numColors=MAXCOLORS, seed=seed)
    ai = AI()
    render(game, aiGame)

    # loop count variables:
    numTicks = 0
    timeSinceIncrement = 0
    pressedKeys = [-1, -1, -1, -1] # up, down, left, right
    while not game.lost or aiGame.lost: # game loop ends when game is lost
        
        updated = handleInput(game, pressedKeys, numTicks)
        while aiGame.numTurns < game.numTurns:
            ai.ai(aiGame)
            aiGame.incrementTime()
            if game.numTurns - aiGame.numTurns % 10 == 0 or game.numTurns - aiGame.numTurns % 5 < 10:
                render(game, aiGame)
        if updated:
            render(game, aiGame)
        if timeSinceIncrement > DELAY: # number of ticks between time increments
            game.incrementTime()
            timeSinceIncrement = 0
            render(game, aiGame)

        FPSCLOCK.tick(FPS)
        numTicks += 1
        timeSinceIncrement += 1
    
    return "Game Over" if game.lost else "You Win!"

def handleInput(game, pressedKeys, numTicks):
    updated = False
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
            updated = True
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
    if numTicks % 2:
        THRESHOLD = 5 # in ticks
        for i in range(len(pressedKeys)):
            pressedKeys[i] += 1 if pressedKeys[i] != -1 else 0
        if pressedKeys[0] > THRESHOLD: # only every other tick
            game.rotateActiveClockwise()
            updated = True
        if pressedKeys[1] > THRESHOLD:
            game.incrementTime()
            updated = True
            timeSinceIncrement = 0
        if pressedKeys[2] > THRESHOLD:
            game.translateActiveLeft()
            updated = True
        if pressedKeys[3] > THRESHOLD:
            game.translateActiveRight()
            updated = True
    
    return updated


def playEndMenu(response):
    DISPLAYSURF.fill(BGCOLOR)

    text = response
    drawText(text, BIGFONT, TEXTSHADOWCOLOR, (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 30), True)
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
    if center: textRect.center = location
    else: textRect.topleft = location
    DISPLAYSURF.blit(textSurf, textRect)


def drawStatus(score, level, piece, location):
    #pygame.draw.rect(DISPLAYSURF, BGCOLOR, pygame.Rect(location + (100, 100)))
    drawText("Score: %s" % score, BASICFONT, TEXTCOLOR, location)
    drawText("Level: %s" % level, BASICFONT, TEXTCOLOR, (location[0], location[1] + 30))
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

    # draw the border and box
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (location[0], location[1], (len(board[0]) * BOXSIZE + BORDER), (len(board) * BOXSIZE + BORDER)), BORDER)
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
    #pygame.draw.rect(DISPLAYSURF, BGCOLOR, pygame.Rect(location + (100, 100)))
    drawText("Next: ", BASICFONT, TEXTCOLOR, location)
    
    # draw 'little board'
    grid = [[Tile() for j in range(DIMENSIONS[0])] for i in range(DIMENSIONS[1])]
    for loc in piece:
        grid[loc[0] + 1][loc[1]] = Tile(state=2, pivot=loc[2], color=color) # 1 is the vertical offset
    drawBoard(grid, (location[0], location[1] + 25))


def render(game, aiGame):
    DISPLAYSURF.fill(BGCOLOR)
    drawText("Player (you):", BASICFONT, TEXTCOLOR, (50, 10), center=False)
    drawText("AI (them):", BASICFONT, TEXTCOLOR, (WINDOWWIDTH + 50, 10), center=False)
    drawBoard(game.getBoard(), (50, 50))
    drawBoard(aiGame.getBoard(), (WINDOWWIDTH/2 + 50, 50))
    drawNextPiece(game.PIECES[game.next - 1], game.nextColor, (WINDOWWIDTH/2 - 150, 150))
    drawNextPiece(aiGame.PIECES[aiGame.next - 1], aiGame.nextColor, (WINDOWWIDTH - 150, 150))
    drawStatus(game.numTurns, game.numLines, game.next, (WINDOWWIDTH/2 - 150, 50))
    drawStatus(aiGame.numTurns, aiGame.numLines, aiGame.next, (WINDOWWIDTH - 150, 50))
    pygame.display.update()




if __name__ == "__main__":
    print("Use --silent for mute")
    main()

