from tetris.tetris import Tetris
import random, time
import numpy as np

from ai.utils.utils import getActivePosition, findPositions, isOutOfBounds
from ai.utils.pathfinding import findPath

import ai.utils.display as disp

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

CHANCEOFSURVIVAL = 0.1
CHANCEOFMUTATE = 0.8
INITIALPOP = 10
DESIREDSCORE = 1000

class Player:
	def __init__(self, weights = [0, 0, 0]):
		self.wHeight = weights[0]
		self.wNeighbors = weights[1]
		self.wHoles = weights[2]

	def giveRandomWeights(self):
		self.wHeight = random.uniform(-5, 5)
		self.wNeighbors = random.uniform(-5, 5)
		self.wHoles = random.uniform(-5, 5)

	# this is for comparing players to each other visually
	def name(self):
		return f"{int(self.wHeight*10):02d}:{int(self.wNeighbors*10):02d}:{int(self.wHoles*10):02d}"

	def findHeight(self, board):
		height = 3
		for r in range(len(board)):
			for tile in board[r]:
				if tile.isInactive(): return len(board) - r
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
		# Execute move sequence:
		numPieces = game.numPieces
		while numPieces == game.numPieces:
			if len(moves) > 0:
				if moves[0] == 'd':
					del moves[0]
					game.incrementTime()
				elif moves[0] == 'r':
					del moves[0]
					game.translateActiveRight()
				elif moves[0] == 'l':
					del moves[0]
					game.translateActiveLeft()
				elif moves[0] == 'u':
					del moves[0]
					game.rotateActiveClockwise()
			else:
				game.incrementTime()

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
	p3.wHeight = random.choice([p1.wHeight, p2.wHeight])
	p3.wNeighbors = random.choice([p1.wNeighbors, p2.wNeighbors])
	p3.wHoles = random.choice([p1.wHoles, p2.wHoles])
	return p3

def mutate(p):
	token = random.uniform(-1, 1)
	p.wHeight = p.wHeight + token

	token = random.uniform(-1, 1)
	p.wNeighbors = p.wNeighbors + token

	token = random.uniform(-1, 1)
	p.wHoles = p.wHoles + token

	return p

def evolve(pop, pop_scores):
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
		j = random.randint(0, newGenSize - 1)
		k = j
		while(j == k):
			k = random.randint(0, newGenSize - 1)
		p1 = newGen[j]
		p2 = newGen[k]

		newGen.append(breed(p1, p2))

	return newGen

def train(pop):
	#each player plays the game until death
	#if any player plays well enough (>= DESIREDSCORE), then return tuple (score, player)
	#otherwise, evolve them and return highest score and new generation (highest score, new gen)
	scores = []
	highestScore = 0
	seed = int(round(time.time() * 1000)) 
	print(f"Pop: {[player.name() for player in pop]}")
	
	for player in pop:
		game = Tetris(numColumns=10, numRows=10, seed=seed) # Use the same seed for each player, for fairness
		while(not game.lost):
			player.ai(game) #play round of game
			#disp.clear()
			#print(f"Playing: {player.name()}")
			#print(f"Lines: {game.numLines}")
			#disp.display(game.getBoard(), clear=False)
		print(f"{player.name()} played game with score {game.numLines}.")
		scores.append(game.numLines)
	
	newGen = evolve(pop, scores)
	return (max(scores), newGen)

def save(player):
	f = open("mlmodel",'w+')
	f.write(str(player.wHeight) + "\n")
	f.write(str(player.wNeighbors) + "\n")
	f.write(str(player.wHoles) + "\n")
	f.close()

def main():
	pop = create_initial_population(INITIALPOP)
	popnum = 0
	while(True):
		popnum += 1
		data = train(pop)
		print(f"pop num: {popnum}")
		print(f"best score so far: {data[0]}")
		if(data[0] >= DESIREDSCORE):
			final_player = data[1]
			print("success")
			break
		else:
			pop = data[1]

	save(final_player)

main()

