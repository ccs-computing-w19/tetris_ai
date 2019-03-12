#!/usr/bin/env python3

from tetris.tetris import Tetris, Tile
import pygame, sys, random, time

from drawing.utils import *
from drawing.color import *
from drawing.drawing import *

FPS = 60
WINDOWWIDTH = 960
WINDOWHEIGHT = 600
MAXCOLORS = 360

def main():
    global FPSCLOCK, BASICFONT, BIGFONT, DISPLAYSURF, drawing
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 72)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    drawing = Drawing(pygame, DISPLAYSURF, WINDOWWIDTH, WINDOWHEIGHT)

    pygame.display.set_caption("Enomino")
    playMenu(drawing, "Enomino")
    while True:
        response = playGame()
        playMenu(drawing, response)

from ai.ai import AI
def playGame():
    seed = int(time.time())
    game = Tetris(numColors=MAXCOLORS, seed=seed)
    aiGame = Tetris(numColors=MAXCOLORS, seed=seed)
    ai = AI()
    render(game, aiGame)

    DELAY = 20 # delay between each incrementTime

    # loop count variables:
    numTicks = 0
    timeSinceIncrement = 0
    level = 0
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
        if game.numLines // 10 > level: 
            level = game.numLines // 10
            DELAY = DELAY * 0.8

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


def playMenu(drawing, text):
    drawing.fill()
    drawing.drawMenu(text, BIGFONT, BASICFONT)

    ready = False
    while not ready: # start screen loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                terminate() # exit game
            if event.type == pygame.KEYDOWN:
                ready = True
        pygame.display.update()
        FPSCLOCK.tick()


def render(game, aiGame):
    drawing.fill()
    drawing.drawText(text="Player (you):", font=BASICFONT, location=(50, 10), center=False)
    drawing.drawText(text="AI (them):", font=BASICFONT, location=(WINDOWWIDTH/2 + 50, 10), center=False)
    drawing.drawBoard(board=game.getBoard(), numColors=MAXCOLORS, location=(50, 50), bordersize=5, boxsize=25)
    drawing.drawBoard(board=aiGame.getBoard(), numColors=MAXCOLORS, location=(WINDOWWIDTH/2 + 50, 50), bordersize=5, boxsize=25)
    drawing.drawNextPiece(piece=game.PIECES[game.next - 1], numColors=MAXCOLORS, font=BASICFONT, color=game.nextColor, location=(WINDOWWIDTH/2 - 150, 150), bordersize=5, boxsize=25)
    drawing.drawNextPiece(piece=aiGame.PIECES[aiGame.next - 1], numColors=MAXCOLORS, font=BASICFONT, color=aiGame.nextColor, location=(WINDOWWIDTH - 150, 150), bordersize=5, boxsize=25)
    drawing.drawStatus(score=game.numTurns, level=game.numLines, piece=game.next, font=BASICFONT, location=(WINDOWWIDTH/2 - 150, 50))
    drawing.drawStatus(score=aiGame.numTurns, level=aiGame.numLines, piece=aiGame.next, font=BASICFONT, location=(WINDOWWIDTH - 150, 50))
    pygame.display.update()

if __name__ == "__main__":
    print("Use --silent for mute")
    main()

