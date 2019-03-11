from tetris.tetris import Tetris
import random, time
import numpy as np

from ai.utils.utils import getActivePosition, findPositions, isOutOfBounds
from ai.utils.pathfinding import findPath
from ai.algorithms.mlAi import choosePosition

from ai.utils.display import display, clear

from ml.utils.heuristics import *

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
CHANCEOFMUTATE = 0.2
INITIALPOP = 50
DESIREDSCORE = 1000

class Player:
	def __init__(self, weights=None):
		self.weights = weights if weights != None else [0, 0, 0, 0]

	def giveRandomWeights(self):
		for w in range(len(self.weights)):
			self.weights[w] = random.random() * 10 - 5

	# this is for comparing players to each other visually
	def name(self):
		name = ""
		for weight in self.weights:
			name += f"{int(weight*10):02d}:"
		return name

	def ai(self, game): #mutator function
		board = game.getBoard()
		position = getActivePosition(board, game.pivot)
		positions = findPositions(board, position, game.rotatable)
		path = None
		p = 0; target = 0
		while path == None:
			# someday get around to fixing this stupid bug:
			if len(positions) < 1:
				path = []; break # set path to empty to deal with error
			p = choosePosition(board, positions, self.weights)
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
			clear()
			print(f"Playing: {self.name()}")
			print(f"Lines: {game.numLines}")
			print(f"Target: {target}")
			print([round(self.weights[0] * findHeight(board) + self.weights[1] * numOfNeighbors(positions[pos], board) + self.weights[2] * numOfHoles(positions[pos], board), 2) for pos in range(len(positions))])
			print(self.weights[0] * findHeight(board) + self.weights[1] * numOfNeighbors(target, board) + self.weights[2] * numOfHoles(target, board))
			print(f"Position#: {p}")
			
			display(game.getBoard(), clear=False)
			print(choosePosition(board, positions, self.weights))
			for i in range(3000000): #slow down the game
				pass

def create_initial_population(count):
	#creates a population of players with random genomes
	pop = []
	for i in range(count):
		player = Player()
		player.giveRandomWeights()
		pop.append(player)
	return pop

def breed(p1, p2):
	p3 = Player()
	p3.weights[0] = random.choice([p1.weights[0], p2.weights[0]])
	p3.weights[1] = random.choice([p1.weights[1], p2.weights[1]])
	p3.weights[2] = random.choice([p1.weights[2], p2.weights[2]])
	return p3

def mutate(p):
	p.weights[0] = p.weights[0] + random.uniform(-1, 1)
	p.weights[1] = p.weights[1] + random.uniform(-1, 1)
	p.weights[2] = p.weights[2] + random.uniform(-1, 1)
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
	seed = random.randint(1, 1000000) #int(round(time.time() * 1000))
	print(f"Pop: {[player.name() for player in pop]}")
	
	for player in pop:
		game = Tetris(numColumns=10, numRows=10, seed=seed) # Use the same seed for each player, for fairness
		while(not game.lost):
			player.ai(game) #play round of game
		print(f"{player.name()} played game with score {game.numLines}.", player.weights)
		scores.append(game.numLines)
	
	newGen = evolve(pop, scores)
	return (max(scores), newGen)

def save(player):
	f = open("ml/model",'w+')
	for weight in player.weights:
		f.write(str(weight) + "\n")
	f.close()

def main():
	pop = create_initial_population(INITIALPOP)
	for player in pop:
		print(player.name())
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

if __name__ == "__main__":
	random.seed(3)
	main()

