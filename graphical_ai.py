#from graphical_game import playStartMenu, playEndMenu
import graphical_game as view

import tetris
import pygame

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


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    view.FPSCLOCK = FPSCLOCK
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    view.DISPLAYSURF = DISPLAYSURF
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    view.BASICFONT = BASICFONT
    BIGFONT = pygame.font.Font('freesansbold.ttf', 72)
    view.BIGFONT = BIGFONT
    pygame.display.set_caption('Enomino')

    view.playStartMenu()
    while True:
        playGame()
        view.playEndMenu()


def playGame():
    game = tetris.Tetris(numColors=MAXCOLORS)
    view.render(game)

    # loop count variables:
    numTicks = 0
    timeSinceIncrement = 0

    while not game.lost: # game loop ends when game is lost
        
        # increment time (move blocks down)
        if timeSinceIncrement > 30: # number of ticks between time increments
            #game.rotateActiveClockwise()
            #game.incrementTime()
            #game.translateActiveLeft()
            #game.translateActiveRight()

            game.incrementTime()
            timeSinceIncrement = 0
            view.render(game)

        pygame.display.update()

        FPSCLOCK.tick(view.FPS)
        numTicks += 1
        timeSinceIncrement += 1




if __name__ == "__main__":
    main()


