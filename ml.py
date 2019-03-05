from tetris.tetris import Tetris
import random
import numpy as np

from ai.utils.utils import getActivePosition, findPositions, isOutOfBounds
from ai.utils.pathfinding import findPath

#use genetic algorithm to find weights for specified parametersto calculate which position to choose

#concept:
#we start with a batch of "players", a collection of weights for the paramters
#play the game and the ones with higher scores (more fit) are the better ones
#breed and mutate

#parameters:
#height
#neighbors
#holes
#represented as [height, neighbors, holes]

#need to implement:
#get score from end of a game
#make the ai play the game

CHANCEOFSURVIVAL = 0.2
CHANCEOFMUTATE = 0.25
INITIALPOP = 30
DESIREDSCORE = 500

class Player:
	def __init__(self, weights = [0, 0, 0]):
		self.wHeight = weights[0]
		self.wNeighbors = weights[1]
		self.wHoles = weights[2]

	def giveRandomWeights(self):
		self.wHeight = random.uniform(-5, 5)
		self.wNeighbors = random.uniform(-5, 5)
		self.wHoles = random.uniform(-5, 5)

	def findHeight(self, board):
		height = 0
		for r in range(len(board)):
			if(1 in board[r]):
				height = len(board) - r
				break
		return height

	def numOfNeighbors(self, position, board):
		neighborCount = 0
		for point in position:
			if isOutOfBounds(board, (point[0] - 1, point[1])) or board[point[0] - 1][point[1]].isInactive(): neighborCount += 1
			if isOutOfBounds(board, (point[0] + 1, point[1])) or board[point[0] + 1][point[1]].isInactive(): neighborCount += 1
			if isOutOfBounds(board, (point[0], point[1] - 1)) or board[point[0]][point[1] - 1].isInactive(): neighborCount += 1
			if isOutOfBounds(board, (point[0], point[1] + 1)) or board[point[0]][point[1] + 1].isInactive(): neighborCount += 1
		return neighborCount

	def numOfHoles(self, position, board):
		holes = 0
		for r in range(len(board)):
			for c in range(len(board[r])):
				if(not isOutOfBounds(board, (r - 1, c)) and board[r-1][c].isInactive()):
					holes += 1
		return holes

	def choosePosition(self, positions, board):
		positionScores = []
		bestPosIndex = -1
		for pos in positions:
			positionScores.append(self.wHeight * self.findHeight(board) + self.wNeighbors * self.numOfNeighbors(pos, board) + self.wHoles * self.numOfHoles(pos, board))
		bestPosScore = max(positionScores)
		numOfPositions = len(positions)
		for i in range(numOfPositions):
			if(positionScores[i] == bestPosScore):
				bestPosIndex = i
		return bestPosIndex

	def ai(self, game): #mutator function
		board = game.getBoard()
		position = getActivePosition(board, game.pivot)
		positions = findPositions(board, position, game.rotatable)
		path = None
		while path == None:
			# someday get around to fixing this stupid bug:
			if len(positions) < 1:
				path = []; break # set path to empty to deal with error
			p = self.choosePosition(positions, board)
			target = positions[p]
			del positions[p] # remove from list of remaining positions
			path = findPath(board, position, target, game.rotatable)
		moves = path
		# Essentially, handle input:
		while len(moves) > 0:
			if moves[0] == 'd':
				del moves[0]
				return
			elif moves[0] == 'r':
				del moves[0]
				game.translateActiveRight()
			elif moves[0] == 'l':
				del moves[0]
				game.translateActiveLeft()
			elif moves[0] == 'u':
				del moves[0]
				game.rotateActiveClockwise()

def create_initial_population(count):
	#creates a population of players with random genomes
	pop = []
	for i in range(count):
		p = Player()
		p.giveRandomWeights()
		pop.append(p)
	return pop

def breed(p1, p2):
	p3 = Player()
	p3.wHeight = random.choice(p1.wHeight, p2.wHeight)
	p3.wNeighbors = random.choice(p1.wNeighbors, p2.wNeighbors)
	p3.wHoles = random.choice(p1.wHoles, p2.wHoles)
	return p3

def mutate(p):
	token = random.uniform(-3, 3)
	p.wHeight = p.wHeight + token

	token = random.uniform(-3, 3)
	p.wNeighbors = p.wNeighbors + token

	token = random.uniform(-3, 3)
	p.wHoles = p.wHoles + token

	return p

def evolve(pop):
	#first make each of them play the game ***

	pop_scores = []
	for p in pop:
		pop_scores.append(p.get_score())

	#take top half of them and some random ones from the weak half
	genSize = len(pop)
	median = np.median(pop_scores)

	newGen = []
	for i in range(genSize):
		if(pop_scores[i] >= median):
			newGen.append(pop[i])
		elif(CHANCEOFSURVIVAL > random.random()):
			newGen.append(pop[i])

	#randomly mutate some of them
	newGenSize = len(newGen)
	for i in range(newGenSize):
		if(CHANCEOFMUTATE > random.random()):
			newGen[i] = mutate(newGen[i])

	emptyPop = genSize - newGenSize

	for i in range(emptyPop):
		j = random.randint(0, newGenSize)
		k = j
		while(j == k):
			k = random.randint(0, newGenSize)
		p1 = newGen[j]
		p2 = newGen[k]

		newGen.append(breed(p1, p2))

	return newGen

def playRound(game, player):
	#player plays a around of the game and returns the updated score and state of game (ongoing or lost) return a tuple(game, score, gamestate)
	player.ai(game)
	game.incrementTime()

def train(pop):
	#each player plays the game until death
	#if any player plays well enough (>= DESIREDSCORE), then return tuple (score, player)
	#otherwise, evolve them and return highest score and new generation (highest score, new gen)
	
	highestScore = 0
	for p in pop:
		game = Tetris()
		lost = False
		score = 0
		while(not lost):
			playRound(game, p)
			lost = game.lost
			score = game.numLines
			if(score >= DESIREDSCORE):
				return (score, p)
		if(score > highestScore):
			highestScore = score

	newGen = evolve(pop)
	return (highestScore, newGen)

def save(player):
	f = open("mlmodel",'w+')
	f.write(str(player.wHeight) + "\n")
	f.write(str(player.wNeighbors) + "\n")
	f.write(str(player.wHoles) + "\n")
	f.close()

def main():
	pop = create_initial_population(INITIALPOP)

	while(True):
		data = train(pop)
		if(data[0] >= DESIREDSCORE):
			final_player = data[1]
			print("success")
			break
		else:
			pop = data[1]

	save(final_player)

main()

