from tetris.tetris import Tetris
import random, time, sys
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
INITIALPOP = 10
DESIREDSCORE = 1000
NUMWEIGHTS = 4
VERBOSE = False



class Player:
	def __init__(self, weights=None):
		self.weights = weights if weights != None else [0 for w in range(NUMWEIGHTS)]

	def giveRandomWeights(self):
		for w in range(len(self.weights)):
			self.weights[w] = random.random() * 10 - 5

	# this is for comparing players to each other visually
	def name(self):
		return "(" + " ".join([f'{round(weight, 1): >4}' for weight in self.weights]) + ")"

	def ai(self, game): #mutator function
		board = game.getBoard()
		position = getActivePosition(board, game.pivot)
		positions = findPositions(board, position, game.rotatable)
		path = None
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
	for w in range(len(p3.weights)):
		p3.weights[w] = random.choice([p1.weights[w], p2.weights[w]])
	return p3

def mutate(p):
	for w in range(len(p.weights)):
		p.weights[w] = p.weights[w] + random.uniform(-1, 1)
	return p

def evolve(pop, pop_scores, base):
	#take top half of them and some random ones from the weak half
	genSize = len(pop)

	for i in range(genSize):
		pop_scores[i] += random.random() # add random fuzz
	median = np.median(pop_scores)
	
	newGen = []
	for i in range(genSize):
		if (pop_scores[i] > median):
			newGen.append(pop[i])
			if VERBOSE: print(pop[i].name(), int(pop_scores[i]), "SURVIVED")
		elif (CHANCEOFSURVIVAL > random.random()):
			newGen.append(mutate(pop[i]))
			if VERBOSE: print(pop[i].name(), int(pop_scores[i]), "SQUEAKED BY")
		else:
			if VERBOSE: print(pop[i].name(), int(pop_scores[i]), "DIED")

	print("Median score:", int(median), f"(relative to baseline: {round(int(median)/(base+10**(-10)) * 100)}%)")

	while len(newGen) < genSize:
		a, b = random.randint(0, len(newGen) - 1), random.randint(0, len(newGen) - 1)
		while a == b:
			b = random.randint(0, len(newGen) - 1)
		newGen.append(mutate(breed(newGen[a], newGen[b])))
	
	return newGen

from ai.algorithms.holyNeighborAi import choosePosition as baselineFunction
from ai.ai import AI
def baseline(seed):
	random.seed(seed)
	game = Tetris(numColumns=10, numRows=10)
	baselineAI = AI(baselineFunction)
	while(not game.lost):
		baselineAI.aiSequence(game)
	random.seed()

	if VERBOSE: print(f"Baseline AI played game with score {game.numLines}.")
	return game.numLines

def train(population, seed):
	#each player plays the game until death
	#if any player plays well enough (>= DESIREDSCORE), then return tuple (score, player)
	#otherwise, evolve them and return highest score and new generation (highest score, new gen)
	scores = []
	highestScore = 0
	bestPlayer = 0

	for player in population:
		random.seed(seed)
		game = Tetris(numColumns=10, numRows=10) # Use the same seed for each player, for fairness
		while(not game.lost):
			player.ai(game) #play round of game
		random.seed() # reset random seed

		if game.numLines > highestScore:
			highestScore = game.numLines
			bestPlayer = player

		if VERBOSE: print(f"{player.name()} played game with score {game.numLines}.", player.weights)
		scores.append(game.numLines) # adds random element to make a continuum of values

	print(f"{bestPlayer.name()} is the best player with a score of {highestScore}: {bestPlayer.weights}")
	return scores

def save(player):
	f = open("ml/model",'w+')
	for weight in player.weights:
		f.write(str(weight) + "\n")
	f.close()

def main(popCount):
	pop = create_initial_population(popCount if popCount else INITIALPOP)

	if VERBOSE: 
		print("\nInitial Population:")
		for player in pop: print(player.name())
	
	popnum = 1
	while(True):
		seed = random.randint(1, 10**10)
		print(f"\nPopulation {popnum}:")
		base = baseline(seed)
		scores = train(pop, seed)
		if VERBOSE: print("\n")
		pop = evolve(pop, scores, base)
		popnum += 1
	
	save(final_player)

if __name__ == "__main__":
	count = None
	if "-v" in sys.argv:
		sys.argv.remove("-v")
		VERBOSE = True
	if len(sys.argv) > 1 and sys.argv[1].isnumeric():
		count = int(sys.argv[1])
		del sys.argv[1]
	if len(sys.argv) != 1:
		print("Usage: python3 train_ml.py [-v] [count]")
		exit(0)
	main(popCount=count)
	

	

