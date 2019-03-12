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
from ai.algorithms.mlAi import choosePosition as func1
from ai.algorithms.holyNeighborAi import choosePosition as func2
def playGame():
    game = Tetris(numColors=MAXCOLORS, seed=int(time.time()))
    ai = AI(func1)

    game2 = Tetris(numColors=MAXCOLORS, seed=int(time.time()))
    ai2 = AI(func2)

    render(game, game2)

    # loop count variables:

    pressedKeys = [-1, -1, -1, -1] # up, down, left, right
    while not game.lost and not game2.lost: # game loop ends when game is lost
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT:
                terminate() # exit game
        
        # increment time (move blocks down)
        ai.aiSequence(game)
        ai2.aiSequence(game2)
        render(game, game2)

        FPSCLOCK.tick(FPS)
    return "Player 2 (Will) won" if game.lost else "Player 1 (Bill) won"

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
    drawing.drawText(text="AI #1 (Bill):", font=BASICFONT, location=(50, 10), center=False)
    drawing.drawText(text="AI #2 (Will):", font=BASICFONT, location=(WINDOWWIDTH/2 + 50, 10), center=False)
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

