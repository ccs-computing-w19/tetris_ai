#!/usr/bin/env python3

from tetris.tetris import Tetris
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
    

from ai.ai import AI
def playGame():
    game = Tetris(numColors=MAXCOLORS)
    ai = AI()
    # loop count variables:
    numTicks = 0
    while not game.lost: # game loop ends when game is lost
        ai.ai(game)
        game.incrementTime()
        numTicks += 1
    return game.numLines


if __name__ == "__main__":
    main()

