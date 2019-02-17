#!/usr/bin/env python3

import tetris
import pygame, sys
from math import pi, sin
import random

import progressbar

MAXCOLORS = 1
N = 100

def main():
    # progress bar:
    bar = progressbar.ProgressBar(maxval=N, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    sumLines = 0
    for i in range(N):
        bar.update(i)
        sumLines += playGame()
    bar.update(N)
    print("AI Ability:", sumLines / N)

def playGame():
    game = tetris.Tetris(numColors=MAXCOLORS)
    # loop count variables:
    numTicks = 0
    # set up ai:
    moves = []
    numPieces = 0
    while not game.lost: # game loop ends when game is lost
        moves, numPieces = ai(game, moves, numPieces)
        game.incrementTime()
        numTicks += 1
    return game.numLines


import copy
from ai.utils.utils import getActivePosition, findPositions
from ai.utils.pathfinding import findPath
from ai.utils.display import display
from ai.holyNeighborAi import choosePosition
def ai(game, moves, numPieces):
    if game.numPieces > numPieces:
        position = getActivePosition(game.getBoard(), game.pivot)
        positions = findPositions(game.getBoard(), position, game.rotatable)
        path = None
        while path == None: # find non-null path
            if len(positions) < 1:
                display(game.getBoard(), position, False)
                print("ERROR: COULDN'T FIND ANY VALID POSITIONS")
            target = choosePosition(game.getBoard(), positions)
            path = findPath(game.getBoard(), position, target, game.rotatable)
        moves = path
        numPieces += 1
    # Essentially, handle input:
    while len(moves) > 0:
        if moves[0] == 'd':
            del moves[0]
            return moves, numPieces
        elif moves[0] == 'r':
            del moves[0]
            game.translateActiveRight()
        elif moves[0] == 'l':
            del moves[0]
            game.translateActiveLeft()
        elif moves[0] == 'u':
            del moves[0]
            game.rotateActiveClockwise()
    return moves, numPieces


if __name__ == "__main__":
    main()

