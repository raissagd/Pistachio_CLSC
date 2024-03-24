from abc import ABC, abstractmethod
import numpy as np
import copy

class Neighbourhood(ABC):
    """
    Abstract class for Neighbourhood Search Algorithms.
    """
    def __init__(self, solution):
        self.chromosomes = [f"S{i}" for i in range(1, 9)] # List of chromosomes (S1, S2, ..., S8)
        self.solution = copy.deepcopy(solution) # Copy of the solution object
        self.chromosome = None # Chromosome, that will be randomly chosen

    def selectRandomChromosome(self):
        attr = np.random.choice(self.chromosomes)  # Select a random chromosome (S1, S2, ..., S8)
        self.chromosome = getattr(self.solution, attr)  # Save the list of numbers associated with that chromosome
    
    def selectRandomPair(self):
        i, j = sorted(np.random.permutation(len(self.chromosome))[:2]) # Select two random indices i and j
        return i, j
    
    @abstractmethod
    def applyChange(self):
        pass

class Swap(Neighbourhood):
    """
    Two units of a solution are selected randomly and their positions are swapped. 
    """
    def applyChange(self, N):
        self.selectRandomChromosome()
        for _ in range(N):
            i, j = self.selectRandomPair()
            self.chromosome[i], self.chromosome[j] = self.chromosome[j], self.chromosome[i] # Swap the elements at indices i and j

class Reversion(Neighbourhood):
    """
    In addition to Swap, units located between swapped units are reversed, too.
    """
    def applyChange(self, N):
        self.selectRandomChromosome()
        for _ in range(N):
            i, j = self.selectRandomPair()
            start = min(i, j)
            end = max(i, j) + 1
            self.chromosome[start:end] = self.chromosome[start:end][::-1]  # Reverse the selected portion of the chromosome

class Insertion(Neighbourhood):
    """
    Two units of a solution are selected randomly. The unit in the second position is placed immediately after the 
    unit in the first location and the other units are shifted to the right hand side accordingly.
    """
    
    def applyChange(self, N):
        self.selectRandomChromosome()
        for _ in range(N):
            i, j = self.selectRandomPair()
            
            # Ensure i < j
            if i > j:
                i, j = j, i
                
            unit_to_insert = self.chromosome[j] # Extract the unit to be inserted
            
            # Move all units from j-1 to i+1 one position to the right
            for k in range(j, i, -1):
                self.chromosome[k] = self.chromosome[k - 1]
            
            self.chromosome[i + 1] = unit_to_insert # Insert the unit in its new position

class MaxMinSwap(Neighbourhood):
    """
    The units with maximum and minimum values are chosen and their positions are exchanged. 
    """
    def applyChange(self):
        self.selectRandomChromosome()
        min_index = np.argmin(self.chromosome)  # Find the index of the minimum value
        max_index = np.argmax(self.chromosome)  # Find the index of the maximum value
            
        # Swap the elements at indices min_index and max_index
        self.chromosome[min_index], self.chromosome[max_index] = self.chromosome[max_index], self.chromosome[min_index]

class Slide(Neighbourhood):
    """
    1) Two units of a solution are selected randomly. 
    2) The first unit is eliminated.
    3) The other units, located in between the first and the second one, are shifted to the left hand side accordingly.
    4) The first number is placed in the position the second number used to take. 
    """
    def applyChange(self, N):
        self.selectRandomChromosome()
        for _ in range(N):
            i, j = self.selectRandomPair()
            
            # Ensure i < j
            if i > j:
                i, j = j, i
                        
            unit_to_move = self.chromosome[i] # Extract the unit to be moved
            
            # Shift units to the left
            for k in range(i, j):
                self.chromosome[k] = self.chromosome[k + 1]
            
            self.chromosome[j] = unit_to_move  # Place the moved unit in its new position


class ETN(Neighbourhood):
    """
    ETN (Exchange Two Neighbors):
    Two neighbor units of a solution are selected randomly. Their positions are then changed with each other. 
    """
    def applyChange(self, N):
        pass

class RS(Neighbourhood):
    """
    RS (Random Shuffling ):
    A subsequence is chosen (with, for example, 2 elements), then the values of its positions are exchanged
    with the values of the positions of another subsequence. 
    """
    def applyChange(self, N):
        pass

class SPS(Neighbourhood):
    """
    Swaping a Part of Solution (SPS):
    A subsequence of solutions is selected and then shifted to a new position. 
    """
    def applyChange(self, N):
        pass
    
class SRPS(Neighbourhood):
    """
    Swapping a Reversed Part of Solution (SRPS): 
    Similar to SPS, with the difference that, during the moving process, the elements of the selected subsequence
    are reversed.
    """
    def applyChange(self, Nn):
        pass