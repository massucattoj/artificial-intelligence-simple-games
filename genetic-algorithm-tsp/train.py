# -*- coding: utf-8 -*-
"""
    Udemy Course
    Artificial Intelligence for Simple Games
    Created by Jan Warchocki, Hadelin de Ponteves, Kirill Eremenko, SuperDataScience Team
"""

# import libraries
import numpy as np
from environment import Environment

# Creating the bots
'''
    DNA -> A sequencia de planetas visitados pelo foguete, retornando
    sempre para primeiro planeata ao completar o percurso.
        EX: dna = 3, 1, 2, 0 ( where 0 is the first planet)

    FITNESS = Distancia total percorrida pelo foguete
'''

class Route():

    def __init__(self, dnaLength): # how many planets
        self.dnaLength = dnaLength
        self.dna = list()
        self.distance = 0

        # Initializing the random DNA
        for i in range(self.dnaLength - 1): # how the last gene is always zero -> dnaLength -1
            # dna = 3, 1, 2
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
                inx = self.dna.index(dna2[i])
                self.dna[inx] = previous
                self.dna[i] = dna2[i]


        # Random partial mutations  (after crossover add a little bit of mutation)
        # Prevent that our offspring to be too similar to its parents.
        for i in range(self.dnaLength -1):
            if np.random.rand() <= 0.1:
                previous = self.dna[i]
                rnd_gene = np.random.randint(1, self.dnaLength)
                inx = self.dna.index(rnd_gene)
                self.dna[inx] = previous
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
population = ()


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

        for i in range(dnaLength):
            action = route.dna[i]
            route.distance += env.step(action, 'none') # at the end this variable give the total distance travelled by the rocket










































