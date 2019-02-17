import curses, time
from random import randint

from tetris import Tetris

def display(game, window):
    window.clear()
    window.addstr("\n |" + ("--" * len(game.grid[0])) + "|\n")
    for row in game.grid:
        window.addstr(" |")
        for tile in row:
            window.addstr(str(tile.state) + " ")
            #window.addstr("[]" if tile.state else "  ")
        window.addstr("|\n")
    window.addstr(" |" + ("--" * len(game.grid[0])) + "|\n")
    window.addstr("\n  " + "".join([("[]" if (-1, i, False) in game.PIECES[game.next-1] or (-1, i, True) in game.PIECES[game.next-1] else "  ") for i in range(3, 7)]) + " turns: " + str(game.numTurns))
    window.addstr("\n  " + "".join([("[]" if (0, i, False) in game.PIECES[game.next-1] or (0, i, True) in game.PIECES[game.next-1] else "  ") for i in range(3, 7)]) + " lost: " + str(game.lost))
    window.addstr("\n  " + "".join([("[]" if (1, i, False) in game.PIECES[game.next-1] or (1, i, True) in game.PIECES[game.next-1] else "  ") for i in range(3, 7)]) + " clears: " + str(game.numLines))
    window.addstr("\n  " + "".join([("[]" if (2, i, False) in game.PIECES[game.next-1] or (2, i, True) in game.PIECES[game.next-1] else "  ") for i in range(3, 7)]) + " next: " + str(game.next))
    window.addstr("{}".format(game.pivot))
    window.addstr("\n")

def loadScreen(window):
    # Load screen:
    try:
        window.addstr(" ______________________\n")
        for i in range(10):
            window.addstr(" \n")
        window.addstr("         TETRIS        \n")
        window.addstr("    by Ben and Daniel  \n")
        window.addstr("      press any key    \n")
        for i in range(14):
            window.addstr(" \n")
        window.addstr(" ______________________\n")
    except Exception as e:
        raise Exception('Window too small; (29x24 required)') # Don't! If you catch, likely to hide bugs. 
    while 1:
        try:
            key = window.getkey()
            if key == 'q':
                quit()
            else: #if any other key was pressed
                break
        except Exception as e:
            # No input
            pass

def playScreen(window):
    # Play screen:
    game = Tetris(20, 10)
    display(game, window)
    counter = time.time()
    delay = 1; acceleration = 1
    while 1:
        try:
            key = window.getkey()
            if key == 'q':
                quit()
            if key == 's' or key == 'KEY_DOWN':
                game.incrementTime()
            if key == 'a' or key == 'KEY_LEFT':
                game.translateActiveLeft()
            if key == 'd' or key == 'KEY_RIGHT':
                game.translateActiveRight()
            if key == 'w' or key == 'KEY_UP':
                game.rotateActiveClockwise()
            if key == ' ':
                game.hardDrop()
            if key in ['{}'.format(i) for i in range(8)]:
                if key == '0':
                    game.autoChoice = True
                    game.next = randint(1, 7)
                else:
                    game.autoChoice = False
                    game.next = int(key)
            display(game, window)
        except Exception as e:
            # No input
            current = time.time()
            if counter + delay < current:
                game.incrementTime()
                display(game, window)
                counter = current
                delay = 10 ** (5 - float(acceleration)) / (game.numTurns + 10 ** (5 - float(acceleration)))

def main(window):
    curses.noecho() #stop keys echoing to screen
    window.nodelay(True)
    loadScreen(window) #show load screen
    playScreen(window) #show play screen



if __name__ == '__main__':
    curses.wrapper(main)
