import tetris
from tensorflow import keras
import numpy as np
import random

from ai.utils.utils import isOutOfBounds
from ai.utils.pathfinding import findPath
from ai.utils.display import display

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
#

CHANCEOFSURVIVAL = 0.2
CHANCEOFMUTATE = 0.25

class player:
	def __init__(self, weights = [0, 0, 0]):
		wHeight = weights[0]
		wNeighbors = weights[1]
		wHoles = weights[2]

	def giveRandomWeights(self):
		wHeight = random.uniform(-5, 5)
		wNeighbors = random.uniform(-5, 5)
		wHoles = random.uniform(-5, 5)

	def findHeight(self, position):
		pass

	def numOfNeighbors(self, position):
		pass

	def numOfHoles(self, position):
		pass

	def chooseMove(self, positions):
		positionScores = []
		for pos in positions:
			positionScores.append(wHeight * findHeight(pos) + wNeighbors * numOfNeighbors(pos) + wHoles * numOfHoles(pos))

def create_initial_population(count):
	#creates a population of players with random genomes
	pop = []
	for i in range(count):
		p = player()
		p.giveRandomWeights()
		pop.append(p)
	return pop

def breed(p1, p2):
	p3 = player()
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