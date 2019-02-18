#!/usr/bin/env python3

import tetris
import pygame, sys
from math import pi, sin
import random

MAXCOLORS = 1
N = 10

def main():
    avg = 0
    for i in range(N):
        p = playGame()
        print(f"{i}: {p}")
        avg += p
    print(f"Average: {avg / N}")
    

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


from ai.utils.utils import getActivePosition, findPositions
from ai.utils.pathfinding import findPath
from ai.utils.display import display
from ai.holyNeighborAi import choosePosition
def ai(game, moves, numPieces):
    if game.numPieces > numPieces:
        board = game.getBoard()
        position = getActivePosition(board, game.pivot)
        positions = findPositions(board, position, game.rotatable)
        path = None
        while path == None:
            # someday get around to fixing this stupid bug:
            if len(positions) < 1:
                path = []; break # set path to empty to deal with error
            target = choosePosition(board, positions)
            path = findPath(board, position, target, game.rotatable)
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

