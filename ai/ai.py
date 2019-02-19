from ai.utils.utils import getActivePosition, findPositions
from ai.utils.pathfinding import findPath
from ai.utils.display import display
from ai.algorithms.holyNeighborAi import choosePosition

class AI():

    def __init__(self):
        self.choosePosition = choosePosition
        self.moves = []
        self.numPieces = 0

    # this makes a certain number of moves on the game
    def ai(self, game):
        if game.numPieces > self.numPieces:
            board = game.getBoard()
            position = getActivePosition(board, game.pivot)
            positions = findPositions(board, position, game.rotatable)
            path = None
            while path == None:
                # someday get around to fixing this stupid bug:
                if len(positions) < 1:
                    path = []; break # set path to empty to deal with error
                target = self.choosePosition(board, positions)
                path = findPath(board, position, target, game.rotatable)
            self.moves = path
            self.numPieces += 1
        # Essentially, handle input:
        while len(self.moves) > 0:
            if self.moves[0] == 'd':
                del self.moves[0]
                return
            elif self.moves[0] == 'r':
                del self.moves[0]
                game.translateActiveRight()
            elif self.moves[0] == 'l':
                del self.moves[0]
                game.translateActiveLeft()
            elif self.moves[0] == 'u':
                del self.moves[0]
                game.rotateActiveClockwise()