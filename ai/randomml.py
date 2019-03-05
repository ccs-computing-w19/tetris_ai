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
#make the ai play the game

CHANCEOFSURVIVAL = 0.2
CHANCEOFMUTATE = 0.25
INITIALPOP = 30
DESIREDSCORE = 20

class Player:
	def __init__(self, weights = [0, 0, 0]):
		wHeight = weights[0]
		wNeighbors = weights[1]
		wHoles = weights[2]

	def giveRandomWeights(self):
		wHeight = random.uniform(-5, 5)
		wNeighbors = random.uniform(-5, 5)
		wHoles = random.uniform(-5, 5)

	def findHeight(self, position, board):
		pass

	def numOfNeighbors(self, position, board):
		pass

	def numOfHoles(self, position, board):
		pass

	def chooseMove(self, positions, board):
		positionScores = []
		for pos in positions:
			positionScores.append(wHeight * findHeight(pos, board) + wNeighbors * numOfNeighbors(pos, board) + wHoles * numOfHoles(pos, board))
		bestPosScore = max(positionScores)
		numOfPositions = len(positions)
		for i in range(numOfPositions):
			if(positionScores[i] == bestPosScore):
				bestPos = positions[i]
		return bestPos

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
	pass

def train(pop):
	#each player plays the game until death
	#if any player plays well enough (>= DESIREDSCORE), then return tuple (score, player)
	#otherwise, evolve them and return highest score and new generation (highest score, new gen)
	
	highestScore = 0
	for p in pop:
		#make tetris object
		#tetris = 0;
		lost = false
		score = 0
		while(!lost):
			roundState = playRound(game, p)
			lost = roundState[2]
			score = roundState[1]
			game = roundState[0]
			if(score >= DESIREDSCORE):
				return (score, p)
		if(score > highestScore):
			highestScore = score

	newGen = evolve(pop)
	return (highestScore, newGen)

def save(player):
	#copy down parameters to file
	pass

def main():
	pop = create_initial_population(INITIALPOP)

	while(True):
		data = train(pop)
		if(data[0] >= DESIREDSCORE):
			final_player = data[1]
			break
		else:
			pop = data[1]

	save(final_player)


