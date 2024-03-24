from abc import ABC, abstractmethod
from numpy import random
import copy

class Neighbourhood(ABC):
    def __init__(self, solution):
        self.chromosomes = [f"S{i}" for i in range(1, 9)] # List of chromosomes (S1, S2, ..., S8)
        self.solution = copy.deepcopy(solution) # Copy of the solution object
        self.chromosome = None # Chromosome, that will be randomly chosen

    def selectRandomChromosome(self):
        attr = random.choice(self.chromosomes)  # Select a random chromosome (S1, S2, ..., S8)
        self.chromosome = getattr(self.solution, attr)  # Save the list of numbers associated with that chromosome
    
    def selectRandomPair(self):
        i, j = sorted(random.permutation(len(self.chromosome))[:2]) # Select two random indices i and j
        return i, j
    
    @abstractmethod
    def move(self):
        pass

class Swap(Neighbourhood):
    """
    Two units of a solution are selected randomly and their positions are swapped. 
    """
    def move(self, N):
        self.selectRandomChromosome()
        for n in range(N):
            i, j = self.selectRandomPair()
            print(f"Original solution: {self.chromosome}")
            self.chromosome[i], self.chromosome[j] = self.chromosome[j], self.chromosome[i] # Swap the elements at indices i and j
            print(f"Swapped {self.chromosome[i]} and {self.chromosome[j]}")
            print(f"New solution: {self.chromosome}")

class Reversion(Neighbourhood):
    """
    In addition to swap units located between swapped units are reversed, too.
    """
    def move(self, N):
       pass

class Insertion(Neighbourhood):
    """
    Two units of a solution are selected randomly. The unit in the second position is placed immediately after the unit in the first location 
    and the other units are shifted to the right hand side accordingly.
    """
    
    def move(self, N):
       pass

class MaxMinSwap(Neighbourhood):
    """
    The units with maximum and minimum values are chosen and their positions are exchanged. 
    """
    def move(self, N):
        pass

class Slide(Neighbourhood):
    """
    1) Two units of a solution are selected randomly. 
    2) The first unit is eliminated.
    3) The other units, located in between the first and the second one, are shifted to the left hand side accordingly.
    4) The first number is placed in the position the second number used to take. 

    """
    def move(self, N):
        pass

class ETN(Neighbourhood):
    """
    ETN (Exchange Two Neighbors):
    Two neighbor units of a solution are selected randomly. Their positions are then changed with each other. 
    """
    def move(self, N):
        pass

class RS(Neighbourhood):
    """
    RS (Random Shuffling ):
    A subsequence is chosen (with, for example, 2 elements), then the values of its positions are exchanged
    with the values of the positions of another subsequence. 
    """
    def move(self, N):
        pass

class SPS(Neighbourhood):
    """
    Swaping a Part of Solution (SPS):
    A subsequence of solutions is selected and then shifted to a new position. 
    """
    def move(self, N):
        pass
    
class SRPS(Neighbourhood):
    """
    Swapping a Reversed Part of Solution (SRPS): 
    Similar to SPS, with the difference that, during the moving process, the elements of the selected subsequence
    are reversed.
    """
    def move(self, Nn):
        pass