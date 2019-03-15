#!/usr/bin/env python3

from tetris.tetris import Tetris, Tile
import pygame, sys, random, time

from drawing.color import *
from drawing.drawing import *

FPS = 60
WINDOWWIDTH = 480
WINDOWHEIGHT = 600
MAXCOLORS = 360


INPUT = True
DELAY = 15 # delay between each incrementTime


def switchToAI():
    global INPUT, DELAY
    INPUT = False; DELAY = 0.01

def main():
    global FPSCLOCK, BASICFONT, BIGFONT, DISPLAYSURF, drawing
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 72)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    drawing = Drawing(pygame, DISPLAYSURF, WINDOWWIDTH, WINDOWHEIGHT)

    # play music
    if len(sys.argv) < 2 or not sys.argv[1] == "--silent":
        musicFile = 'resources/music.mp3'
        pygame.mixer.init()
        pygame.mixer.music.load(musicFile)
        pygame.mixer.music.play(-1)
    
    pygame.display.set_caption("Enomino")
    playMenu(drawing, "Enomino")
    while True:
        response = playGame()
        playMenu(drawing, response)

from ai.ai import AI
def playGame():
    game = Tetris(numColors=MAXCOLORS)
    ai = AI()

    # a dictionary of pygame buttons and their functions:
    global AI_BUTTON
    AI_BUTTON = pygame.Rect((WINDOWWIDTH - 122, 300, 50, 30))  # ai enable button

    render(game)

    # loop count variables:
    numTicks = 0
    timeSinceIncrement = 0

    pressedKeys = [-1, -1, -1, -1] # up, down, left, right
    while not game.lost: # game loop ends when game is lost
        
        if INPUT: handleInput(game, pressedKeys, numTicks)
        else:
            for event in pygame.event.get(): # event handling loop
                if event.type == pygame.QUIT:
                    terminate() # exit game
        
        # increment time (move blocks down)
        if timeSinceIncrement > DELAY: # number of ticks between time increments
            
            if not INPUT: ai.ai(game)
            
            game.incrementTime()
            timeSinceIncrement = 0
            render(game)

        FPSCLOCK.tick(FPS)
        numTicks += 1
        timeSinceIncrement += 1
    return "Game Over"

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
            if event.key == pygame.K_BACKQUOTE:
                switchToAI()
            if event.key == pygame.K_0: game.setNextPiece(0)
            if event.key == pygame.K_1: game.setNextPiece(1)
            if event.key == pygame.K_2: game.setNextPiece(2)
            if event.key == pygame.K_3: game.setNextPiece(3)
            if event.key == pygame.K_4: game.setNextPiece(4)
            if event.key == pygame.K_5: game.setNextPiece(5)
            if event.key == pygame.K_6: game.setNextPiece(6)
            if event.key == pygame.K_7: game.setNextPiece(7)
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position
            if AI_BUTTON.collidepoint(mouse_pos):
                switchToAI()

    # deal with held-down keys:
    THRESHOLD = 10 # in ticks
    for i in range(len(pressedKeys)):
        pressedKeys[i] += 1 if pressedKeys[i] != -1 else 0
    if numTicks % 2: # only every other tick
        if pressedKeys[0] > THRESHOLD:
            game.rotateActiveClockwise()
            render(game)
        if pressedKeys[1] > THRESHOLD:
            game.incrementTime()
            render(game)
            timeSinceIncrement = 0
        if pressedKeys[2] > THRESHOLD:
            game.translateActiveLeft()
            render(game)
        if pressedKeys[3] > THRESHOLD:
            game.translateActiveRight()
            render(game)


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


def render(game):
    drawing.fill()
    drawing.drawBoard(board=game.getBoard(), numColors=MAXCOLORS, location=(50, 50), bordersize=5, boxsize=25)
    drawing.drawNextPiece(piece=game.PIECES[game.next - 1], numColors=MAXCOLORS, font=BASICFONT, color=game.nextColor, location=(WINDOWWIDTH - 150, 150), bordersize=5, boxsize=25)
    drawing.drawStatus(score=game.numTurns, level=game.numLines, piece=game.next, font=BASICFONT, location=(WINDOWWIDTH - 150, 50))
    pygame.draw.rect(DISPLAYSURF, drawing.BUTTONCOLOR, AI_BUTTON)  # draw button
    drawing.drawText(text="AI", font=BASICFONT, location=(AI_BUTTON.x + AI_BUTTON.width / 2, AI_BUTTON.y + AI_BUTTON.height / 2), center=True)
    pygame.display.update()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    print("Use --silent for mute")
    main()

