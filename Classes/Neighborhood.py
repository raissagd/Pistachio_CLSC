from abc import ABC, abstractmethod
import numpy as np
import copy


class Neighborhood(ABC):
    """
    Abstract class for Neighborhood Search Algorithms.
    """

    def __init__(self, N):
        self.N = N  # Number of iterations

    def selectRandomChromosome(self, solution):
        # List of chromosomes (S1, S2, ..., S8)
        chromosomes = [f"S{i}" for i in range(1, 9)]
        # Select a random chromosome (S1, S2, ..., S8)
        attr = np.random.choice(chromosomes)
        chromosome = getattr(solution, attr)
        return attr, chromosome

    def selectRandomPair(self, chromosome):
        # Select two random indices i and j
        i, j = sorted(np.random.permutation(len(chromosome))[:2])
        return i, j

    @abstractmethod
    def applyChange(self):
        pass

# Ordinary Neighborhood Structures


class Swap(Neighborhood):
    """
    Two units of a solution are selected randomly and their positions are swapped. 
    """

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)
            i, j = self.selectRandomPair(chromosome)
            # Swap the elements at indices i and j
            chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
            # Update the solution with the modified chromosome
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class Reversion(Neighborhood):
    """
    In addition to Swap, units located between swapped units are reversed, too.
    """

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)
            i, j = self.selectRandomPair(chromosome)
            start = min(i, j)
            end = max(i, j) + 1
            # Reverse the selected portion of the chromosome
            chromosome[start:end] = chromosome[start:end][::-1]
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class Insertion(Neighborhood):
    """
    Two units of a solution are selected randomly. The unit in the second position is placed immediately after the 
    unit in the first location and the other units are shifted to the right hand side accordingly.
    """

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)
            i, j = self.selectRandomPair(chromosome)

            # Ensure i < j
            if i > j:
                i, j = j, i

            unit_to_insert = chromosome[j]  # Extract the unit to be inserted

            # Move all units from j-1 to i+1 one position to the right
            for k in range(j, i, -1):
                chromosome[k] = chromosome[k - 1]

            # Insert the unit in its new position
            chromosome[i + 1] = unit_to_insert
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class Slide(Neighborhood):
    """
    1) Two units of a solution are selected randomly. 
    2) The first unit is eliminated.
    3) The other units, located in between the first and the second one, are shifted to the left hand side accordingly.
    4) The first number is placed in the position the second number used to take. 
    """

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)
            i, j = self.selectRandomPair(chromosome)

            # Ensure i < j
            if i > j:
                i, j = j, i

            unit_to_move = chromosome[i]  # Extract the unit to be moved

            # Shift units to the left
            for k in range(i, j):
                chromosome[k] = chromosome[k + 1]

            # Place the moved unit in its new position
            chromosome[j] = unit_to_move
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class ETN(Neighborhood):
    """
    ETN (Exchange Two Neighbors):
    Two neighbor units of a solution are selected randomly. Their positions are then changed with each other. 
    """

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)
            # Select a random index within the valid range
            i = np.random.randint(0, len(chromosome) - 1)
            j = i + 1  # Select the neighbor of the first unit
            # Swap the elements at indices i and j
            chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class RS(Neighborhood):
    """
    RS (Random Shuffling ):
    A subsequence of the solution is selected randomly. The elements of this subsequence are then shuffled.
    """

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)
            # Select start and end indices for the subsequence
            start, end = sorted(np.random.choice(
                len(chromosome), 2, replace=False))
            subsequence = chromosome[start:end+1]  # Extract the subsequence
            np.random.shuffle(subsequence)  # Shuffle the subsequence randomly
            # Place the shuffled subsequence back into the chromosome
            chromosome[start:end+1] = subsequence
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class SPS(Neighborhood):
    """
    Swapping a Part of Solution (SPS):
    A subsequence of the solution is selected and then shifted to a new position. 
    """

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)
            # Select start and end indices for the first subsequence
            start1, end1 = sorted(np.random.choice(
                len(chromosome), 2, replace=False))
            # Select the new position for the first subsequence
            new_position = np.random.randint(
                0, len(chromosome) - (end1 - start1))
            # Extract the first subsequence
            subsequence1 = chromosome[start1:end1+1]

            # Remove the first subsequence from the chromosome
            remaining_indices = np.concatenate(
                (np.arange(start1), np.arange(end1+1, len(chromosome))))
            chromosome = chromosome[remaining_indices]

            # Make space at the new position for the first subsequence
            chromosome = np.concatenate(
                (chromosome[:new_position], subsequence1, chromosome[new_position:]))
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class SRPS(Neighborhood):
    """
    Swapping a Reversed Part of Solution (SRPS): 
    Similar to SPS, with the difference that, during the moving process, the elements of the first selected subsequence are reversed.
    """

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)
            # Select start and end indices for the first subsequence
            start1, end1 = sorted(np.random.choice(
                len(chromosome), 2, replace=False))
            # Select the new position for the first subsequence
            new_position = np.random.randint(
                0, len(chromosome) - (end1 - start1))
            # Extract the first subsequence
            subsequence1 = chromosome[start1:end1+1]
            subsequence1 = subsequence1[::-1]  # Reverse the first subsequence

            # Remove the first subsequence from the chromosome
            remaining_indices = np.concatenate(
                (np.arange(start1), np.arange(end1+1, len(chromosome))))
            chromosome = chromosome[remaining_indices]

            # Make space at the new position for the first subsequence
            chromosome = np.concatenate(
                (chromosome[:new_position], subsequence1, chromosome[new_position:]))
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy

# Directed Neighborhood Structures (Problem-specific)


class MinMaxSwap(Neighborhood):
    """
    A subset of the chromsome is chosen. The highest number is swapped with the lowest number in that subset.
    """

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)
            # Select start and end indices for the subset
            start, end = sorted(np.random.choice(
                len(chromosome), 2, replace=False))
            subset = chromosome[start:end+1]  # Extract the subset
            # Find the index of the minimum value in the subset
            min_index = np.argmin(subset)
            # Find the index of the maximum value in the subset
            max_index = np.argmax(subset)

            # Swap the elements at indices min_index and max_index within the subset
            subset[min_index], subset[max_index] = subset[max_index], subset[min_index]
            # Place the modified subset back into the chromosome
            chromosome[start:end+1] = subset
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class SourceDepotSwap(Neighborhood):
    """
    SourceDepotSwap:
    One of the sources has its priority changed with one of the depots.
    """

    def __init__(self, N, data):
        super().__init__(N)
        self.data = data

    def numSources(self, chromosome):
        if chromosome == 'S1':
            return self.data.K
        elif chromosome == 'S2':
            return self.data.S
        elif chromosome == 'S3':
            return self.data.E
        elif chromosome == 'S4':
            return self.data.J
        elif chromosome == 'S5':
            return self.data.J
        elif chromosome == 'S6':
            return self.data.I
        elif chromosome == 'S7':
            return self.data.Q
        elif chromosome == 'S8':
            return self.data.E

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            # Select a random chromosome
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)

            # Determine the number of sources for this chromosome
            num_sources = self.numSources(chromosome_attr)

            # Ensure there are at least two sources
            if num_sources < 2:
                continue

            # Divide the chromosome into two subsets
            subset1 = chromosome[:num_sources]
            subset2 = chromosome[num_sources:]

            # Randomly select indices from each subset
            index1 = np.random.randint(0, len(subset1))
            index2 = np.random.randint(0, len(subset2))

            # Swap elements between subsets
            subset1[index1], subset2[index2] = subset2[index2], subset1[index1]

            # Merge the subsets back into the chromosome
            chromosome = np.concatenate((subset1, subset2))

            # Update the solution with the modified chromosome
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class ENS(Neighborhood):
    """
    ENS (Exchange Neighbor Priority):
    Two units with neighbor priorities are selected and their positions are then changed with each other.
    """

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)
            # Select a random value from a normal distribution
            value = np.ceil(np.abs(np.random.normal(
                loc=0, scale=(len(chromosome) * 0.75) / 3)))
            chromosome_list = list(chromosome)
            # Find the index of the selected value
            i = chromosome_list.index(value)
            next_value = value + 1
            if next_value in chromosome:  # Check if the next value exists in the chromosome
                # Find the index of the next value
                j = chromosome_list.index(next_value)
                # Swap the elements at indices i and j
                chromosome_list[i], chromosome_list[j] = chromosome_list[j], chromosome_list[i]
                setattr(solution_copy, chromosome_attr,
                        np.array(chromosome_list))

        return solution_copy
