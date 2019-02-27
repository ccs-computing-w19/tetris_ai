#!/usr/bin/env python3

from tetris.tetris import Tetris
import pygame, sys
from math import pi, sin
import random

MAXCOLORS = 1
N = 50

def main():
    avg = 0
    avgHeight = 0
    for i in range(N):
        result = playGame()
        print(f"{i}: {result}")
        avg += result[0]
        avgHeight += result[1]
    print(f"Average: {avg / N}, Average Height: {avgHeight / N}")
    
from ai.ai import AI
from ai.algorithms.holyNeighborAi import choosePosition as function
def playGame():
    game = Tetris(numColors=MAXCOLORS)
    ai = AI(function)
    # loop count variables:
    numPieces = 0
    sumHeights = 0
    while not game.lost and game.numPieces < 200: # game loop ends when game is lost
        ai.ai(game)
        game.incrementTime()
        if game.numPieces > numPieces:
            sumHeights += height(game)
            numPieces += 1
    return (game.numLines, sumHeights / numPieces)

def isEmpty(line):
    for tile in line:
        if not (tile.isEmpty() or tile.isActive()):
            return False
    return True

def height(game):
    board = game.getBoard()
    line = 0
    while line < len(board) and isEmpty(board[line]):
        line += 1
    return len(board) - line



if __name__ == "__main__":
    main()

