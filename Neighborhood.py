from abc import ABC, abstractmethod
import numpy as np
import copy

class Neighborhood(ABC):
    """
    Abstract class for Neighborhood Search Algorithms.
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

class Swap(Neighborhood):
    """
    Two units of a solution are selected randomly and their positions are swapped. 
    """
    def applyChange(self, N):
        self.selectRandomChromosome()
        for _ in range(N):
            i, j = self.selectRandomPair()
            self.chromosome[i], self.chromosome[j] = self.chromosome[j], self.chromosome[i] # Swap the elements at indices i and j

class Reversion(Neighborhood):
    """
    In addition to Swap, units located between swapped units are reversed, too.
    """
    def applyChange(self, N):
        for _ in range(N):
            self.selectRandomChromosome()
            i, j = self.selectRandomPair()
            start = min(i, j)
            end = max(i, j) + 1
            self.chromosome[start:end] = self.chromosome[start:end][::-1]  # Reverse the selected portion of the chromosome

class Insertion(Neighborhood):
    """
    Two units of a solution are selected randomly. The unit in the second position is placed immediately after the 
    unit in the first location and the other units are shifted to the right hand side accordingly.
    """
    
    def applyChange(self, N):
        for _ in range(N):
            self.selectRandomChromosome()
            i, j = self.selectRandomPair()
            
            # Ensure i < j
            if i > j:
                i, j = j, i
                
            unit_to_insert = self.chromosome[j] # Extract the unit to be inserted
            
            # Move all units from j-1 to i+1 one position to the right
            for k in range(j, i, -1):
                self.chromosome[k] = self.chromosome[k - 1]
            
            self.chromosome[i + 1] = unit_to_insert # Insert the unit in its new position

class MaxMinSwap(Neighborhood):
    """
    The units with maximum and minimum values are chosen and their positions are exchanged. 
    """
    def applyChange(self):
        self.selectRandomChromosome()
        min_index = np.argmin(self.chromosome)  # Find the index of the minimum value
        max_index = np.argmax(self.chromosome)  # Find the index of the maximum value
            
        # Swap the elements at indices min_index and max_index
        self.chromosome[min_index], self.chromosome[max_index] = self.chromosome[max_index], self.chromosome[min_index]

class Slide(Neighborhood):
    """
    1) Two units of a solution are selected randomly. 
    2) The first unit is eliminated.
    3) The other units, located in between the first and the second one, are shifted to the left hand side accordingly.
    4) The first number is placed in the position the second number used to take. 
    """
    def applyChange(self, N):
        for _ in range(N):
            self.selectRandomChromosome()
            i, j = self.selectRandomPair()
            
            # Ensure i < j
            if i > j:
                i, j = j, i
                        
            unit_to_move = self.chromosome[i] # Extract the unit to be moved
            
            # Shift units to the left
            for k in range(i, j):
                self.chromosome[k] = self.chromosome[k + 1]
            
            self.chromosome[j] = unit_to_move  # Place the moved unit in its new position

class ETN(Neighborhood):
    """
    ETN (Exchange Two Neighbors):
    Two neighbor units of a solution are selected randomly. Their positions are then changed with each other. 
    """
    def applyChange(self, N):
        for _ in range(N):
            self.selectRandomChromosome()
            i = np.random.randint(0, len(self.chromosome) - 1)  # Select a random index within the valid range
            j = i + 1  # Select the neighbor of the first unit
            
            self.chromosome[i], self.chromosome[j] = self.chromosome[j], self.chromosome[i]  # Swap the elements at indices i and j

class RS(Neighborhood):
    """
    RS (Random Shuffling ):
    A subsequence of the solution is selected randomly. The elements of this subsequence are then shuffled.
    """
    def applyChange(self, N):
        for _ in range(N):
            self.selectRandomChromosome()
            start, end = sorted(np.random.choice(len(self.chromosome), 2, replace=False)) # Select start and end indices for the subsequence
            
            subsequence = self.chromosome[start:end+1] # Extract the subsequence
            
            np.random.shuffle(subsequence) # Shuffle the subsequence randomly

            self.chromosome[start:end+1] = subsequence # Place the shuffled subsequence back into the chromosome

class SPS(Neighborhood):
    """
    Swapping a Part of Solution (SPS):
    A subsequence of the solution is selected and then shifted to a new position. 
    """
    def applyChange(self, N):
        for _ in range(N):
            self.selectRandomChromosome()
            
            start1, end1 = sorted(np.random.choice(len(self.chromosome), 2, replace=False)) # Select start and end indices for the first subsequence
            
            new_position = np.random.randint(0, len(self.chromosome) - (end1 - start1)) # Select the new position for the first subsequence
                        
            subsequence1 = self.chromosome[start1:end1+1] # Extract the first subsequence
            
            # Remove the first subsequence from the chromosome
            remaining_indices = np.concatenate((np.arange(start1), np.arange(end1+1, len(self.chromosome))))
            self.chromosome = self.chromosome[remaining_indices]
            
            # Make space at the new position for the first subsequence
            self.chromosome = np.concatenate((self.chromosome[:new_position], subsequence1, self.chromosome[new_position:]))
    
class SRPS(Neighborhood):
    """
    Swapping a Reversed Part of Solution (SRPS): 
    Similar to SPS, with the difference that, during the moving process, the elements of the first selected subsequence
    are reversed.
    """
    def applyChange(self, N):
        for _ in range(N):
            self.selectRandomChromosome()
            
            # Select start and end indices for the first subsequence
            start1, end1 = sorted(np.random.choice(len(self.chromosome), 2, replace=False))
            
            # Select the new position for the first subsequence
            new_position = np.random.randint(0, len(self.chromosome) - (end1 - start1))
            
            # Extract the first subsequence
            subsequence1 = self.chromosome[start1:end1+1]
            
            # Reverse the first subsequence
            subsequence1 = subsequence1[::-1]
            
            # Remove the first subsequence from the chromosome
            remaining_indices = np.concatenate((np.arange(start1), np.arange(end1+1, len(self.chromosome))))
            self.chromosome = self.chromosome[remaining_indices]
            
            # Make space at the new position for the first subsequence
            self.chromosome = np.concatenate((self.chromosome[:new_position], subsequence1, self.chromosome[new_position:]))
            print(self.chromosome)
