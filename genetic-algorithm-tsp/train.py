# -*- coding: utf-8 -*-
"""
    Udemy Course - Artificial Intelligence for Simple Games
    Created by Jan Warchocki, Hadelin de Ponteves, Kirill Eremenko, SuperDataScience Team

    Massucatto, Jean
"""

# Import libraries
import numpy as np
from environment import Environment

# Creating the bots
'''
    DNA -> A sequence of visited planets by the rocket, and at the end returned
    to the first planet ( 0 ) to complete the route.
        EX: dna = 3, 1, 2, 0 ( where 0 is the first planet)

    FITNESS = Total distance traveled by the rocket
'''
class Route():

    def __init__(self, dnaLength): # how many planets
        self.dnaLength = dnaLength
        self.dna = list()
        self.distance = 0

        # Initializing the DNA in a random way (random planets)
        for i in range(self.dnaLength - 1): # how the last gene is always zero -> dnaLength -1
            # ex dna = 3, 1, 2
            random = np.random.randint(1, self.dnaLength)
            while random in self.dna:
                random = np.random.randint(1, self.dnaLength)

            self.dna.append(random)
        self.dna.append(0)
        # ex dna = 3, 1, 2, 0

    # Building the crossover method
    ''' Take two DNAs (parents), mix them up and create a new DNA'''
    def mix(self, dna1, dna2):

        self.dna = dna1.copy() # make a copy from dna1

        for i in range(self.dnaLength - 1):

            # select a % of inheritance from one dna to the other (in this case 50%)
            # save the the position where is the gene from dna2 in dna1
            # change the genes
            if np.random.rand() <= 0.5:
                previous = self.dna[i]
                idx = self.dna.index(dna2[i])
                self.dna[idx] = previous
                self.dna[i] = dna2[i]


        # Random partial mutations  (after crossover add a little bit of mutation)
        # Prevent that our offspring to be too similar to its parents.
        for i in range(self.dnaLength -1):
            if np.random.rand() <= 0.1:
                previous = self.dna[i]
                rnd_gene = np.random.randint(1, self.dnaLength)
                idx = self.dna.index(rnd_gene)
                self.dna[idx] = previous
                self.dna[i] = rnd_gene

            elif np.random.rand() <= 0.1:
                rnd = np.random.randint(1, self.dnaLength)
                prevInx = self.dna.index(rnd)
                self.dna.insert(i, rnd)

                if i >= prevInx:
                    self.dna.pop(prevInx)
                else:
                    self.dna.pop(prevInx + 1)


''' Initializing the main code '''
populationSize = 50 # how many bots (number of objects of this route class)
mutationRate = 0.1
nSelected = 5 # number of bots selected to create a new population

# create an object of the environment class
env = Environment()
dnaLength = len(env.planets)
population = list()


# Create the first population
for i in range(populationSize):
    route = Route(dnaLength)
    population.append(route)

# Starting the main loop (iterate over all generations)
generation = 0
bestDist = np.inf
while True:
    generation += 1

    # Evaluating the population
    # For each route object in population
    for route in population:
        env.reset()

        # get the distance planet by planet for that route
        for i in range(dnaLength):
            action = route.dna[i]
            route.distance += env.step(action, 'none') # at the end this variable give the total distance travelled by the rocket

    # Sorting the population (the first step to get the best bot from each population)
    sortedPop = sorted(population, key = lambda x: x.distance)
    population.clear()

    if sortedPop[0].distance < bestDist:
        bestDist = sortedPop[0].distance


    # Add best previous bots to the population (case the new bots presents worst results)
    for i in range(nSelected):
        best = sortedPop[i]
        best.distance = 0

        population.append(best)

    # Filling the rest of the population
    left = populationSize - nSelected

    for i in range(left):
        newRoute = Route(dnaLength)

        # if the new route is a complete mutation (that is a new random parent)
        if np.random.rand() <= mutationRate:
            population.append(newRoute)

        else:
            idx1 = np.random.randint(0, nSelected)
            idx2 = np.random.randint(0, nSelected)
            while idx1 == idx2:
                idx2 = np.random.randint(0, nSelected)

            dna1 = sortedPop[idx1].dna
            dna2 = sortedPop[idx2].dna

            newRoute.mix(dna1, dna2)

            population.append(newRoute)


    # Displaying the results
    env.reset()

    for i in range(dnaLength):
        action = sortedPop[0].dna[i] # next planet to go
        _ = env.step(action, 'normal')

    if generation % 100 == 0:
        env.reset()
        for i in range(dnaLength):
            action = sortedPop[0].dna[i] # next planet to go
            _ = env.step(action, 'beautiful')

    print('Generation: ' + str(generation) + 'Shortest distance: {:.2f}'.format(bestDist) + ' light years')
