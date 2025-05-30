from abc import ABC, abstractmethod
import numpy as np
import copy
import scipy.sparse


class Neighborhood(ABC):
    """
    Abstract class for Neighborhood Search Algorithms.
    """

    def __init__(self, N):
        self.N = N  # Number of iterations
        self.name = self.__class__.__name__  # Name of the class

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

class FixedCostSwap(Neighborhood):
    """
    Performs cost-aware swaps of facility activation states to reduce total fixed opening costs in a supply chain network.
    """

    def __init__(self, N, data):
        super().__init__(N)
        self.data = data  # Store data as an instance attribute

    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            # Select a random chromosome
            chromosome_attr, chromosome = self.selectRandomChromosome(
                solution_copy)

            # Chromosome 1: Pistachio Factories -> Pistachio Consumers (K + N1)
            if chromosome_attr == 'S1':
                opened = np.where(solution_copy.W == 1)[0]
                closed = np.where(solution_copy.W == 0)[0]
                cost_opened = self.data.Fw[opened]
                cost_closed = self.data.Fw[closed]
                i = np.argmax(cost_opened)
                j = np.argmin(cost_closed)
                i = opened[i]
                j = closed[j]
                chromosome_list = list(chromosome)
                # Swap the elements at indices i and j
                chromosome_list[i], chromosome_list[j] = chromosome_list[j], chromosome_list[i]
                setattr(solution_copy, chromosome_attr, np.array(chromosome_list))
            
            # Chromosome 2: Cosmetics Factories -> Cosmetics Consumers (S + N3)
            elif chromosome_attr == 'S2':
                opened = np.where(solution_copy.V == 1)[0]
                closed = np.where(solution_copy.V == 0)[0]
                cost_opened = self.data.Fv[opened]
                cost_closed = self.data.Fv[closed]
                i = np.argmax(cost_opened)
                j = np.argmin(cost_closed)
                i = opened[i]
                j = closed[j]
                chromosome_list = list(chromosome)
                # Swap the elements at indices i and j
                chromosome_list[i], chromosome_list[j] = chromosome_list[j], chromosome_list[i]
                setattr(solution_copy, chromosome_attr, np.array(chromosome_list))
            
            # Chromosome 3: Oil extraction centers -> oil consumers + cosmetics factories (E + N2 + S)
            elif chromosome_attr == 'S3':
                opened_e = np.where(solution_copy.R == 1)[0]
                closed_e = np.where(solution_copy.R == 0)[0]
                cost_opened = self.data.Fr[opened_e]
                cost_closed = self.data.Fr[opened_e]
                i = np.argmax(cost_opened)
                j = np.argmin(cost_closed)
                i = opened_e[i]
                j = closed_e[j]
                chromosome_list = list(chromosome)
                # Swap the elements at indices i and j
                chromosome_list[i], chromosome_list[j] = chromosome_list[j], chromosome_list[i]
                setattr(solution_copy, chromosome_attr, np.array(chromosome_list))
                
            # Chromosome 4: Processing center -> pistachio factories (J + K)
            elif chromosome_attr == 'S4':
                opened = np.where(solution_copy.U == 1)[0]
                closed = np.where(solution_copy.U == 0)[0]
                cost_opened = self.data.Fu[opened]
                cost_closed = self.data.Fu[closed]
                i = np.argmax(cost_opened)
                j = np.argmin(cost_closed)
                i = opened[i]
                j = closed[j]
                chromosome_list = list(chromosome)
                # Swap the elements at indices i and j
                chromosome_list[i], chromosome_list[j] = chromosome_list[j], chromosome_list[i]
                setattr(solution_copy, chromosome_attr, np.array(chromosome_list))
                
            # Chromosome 5: Processing center -> oil extraction center (J + E)
            elif chromosome_attr == 'S5':
                opened = np.where(solution_copy.U == 1)[0]
                closed = np.where(solution_copy.U == 0)[0]
                cost_opened = self.data.Fu[opened]
                cost_closed = self.data.Fu[closed]
                i = np.argmax(cost_opened)
                j = np.argmin(cost_closed)
                i = opened[i]
                j = closed[j]
                chromosome_list = list(chromosome)
                # Swap the elements at indices i and j
                chromosome_list[i], chromosome_list[j] = chromosome_list[j], chromosome_list[i]
                setattr(solution_copy, chromosome_attr, np.array(chromosome_list))
            
            # Chromosome 6: Pistachio producers -> processing centers (I + J)
            elif chromosome_attr == 'S6':
                pass

            # Chromosome 7: Composting centers -> composting consumers (Q + M)
            elif chromosome_attr == 'S7':
                opened = np.where(solution_copy.Y == 1)[0]
                closed = np.where(solution_copy.Y == 0)[0]
                cost_opened = self.data.Fy[opened]
                cost_closed = self.data.Fy[closed]
                i = np.argmax(cost_opened)
                j = np.argmin(cost_closed)
                i = opened[i]
                j = closed[j]
                chromosome_list = list(chromosome)
                # Swap the elements at indices i and j
                chromosome_list[i], chromosome_list[j] = chromosome_list[j], chromosome_list[i]
                setattr(solution_copy, chromosome_attr, np.array(chromosome_list))

            # Chromosome 8: Oil extraction centers -> composting centers (E + Q)
            elif chromosome_attr == 'S8':
                opened = np.where(solution_copy.R == 1)[0]
                closed = np.where(solution_copy.R == 0)[0]
                cost_opened = self.data.Fr[opened]
                cost_closed = self.data.Fr[closed]
                i = np.argmax(cost_opened)
                j = np.argmin(cost_closed)
                i = opened[i]
                j = closed[j]
                chromosome_list = list(chromosome)
                # Swap the elements at indices i and j
                chromosome_list[i], chromosome_list[j] = chromosome_list[j], chromosome_list[i]
                setattr(solution_copy, chromosome_attr, np.array(chromosome_list))
                
                # continue
                
        return solution_copy
    
class TransportCostSwap(Neighborhood):
    """
    Performs cost-aware swaps of facility activation states to reduce total transport costs in a supply chain network.
    """

    def __init__(self, N, data):
        super().__init__(N)
        self.data = data  # Store data as an instance attribute
    
    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        # Helper to swap bits in a 1D binary array
        def swap_bits(arr, idx_remove, idx_add):
            lst = list(arr)
            lst[idx_remove], lst[idx_add] = lst[idx_add], lst[idx_remove]
            return np.array(lst)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(solution_copy)
            row_mask = chromosome  # binary vector representing active(1)/inactive(0)

            # Handle each chromosome type with its cost matrix
            if chromosome_attr == 'S1':  # Pistachio Factories -> Pistachio Consumers
                cost = self.data.Cp
                inactive = np.where(row_mask == 0)[0]
                active = np.where(row_mask == 1)[0]
                if not inactive.size or not active.size:
                    continue
                # cheapest inactive edge
                costs_in = cost[0, inactive]
                j = inactive[np.argmin(costs_in)]
                # most expensive active edge
                costs_ac = cost[0, active]
                k = active[np.argmax(costs_ac)]
                new_chrom = swap_bits(chromosome, k, j)
                setattr(solution_copy, chromosome_attr, new_chrom)

            elif chromosome_attr == 'S2':  # Cosmetics Factories -> Cosmetics Consumers
                cost = self.data.Cl
                inactive = np.where(row_mask == 0)[0]
                active = np.where(row_mask == 1)[0]
                if not inactive.size or not active.size:
                    continue
                j = inactive[np.argmin(cost[0, inactive])]
                k = active[np.argmax(cost[0, active])]
                new_chrom = swap_bits(chromosome, k, j)
                setattr(solution_copy, chromosome_attr, new_chrom)

            elif chromosome_attr == 'S3':  # Oil extraction -> consumers + factories
                # E -> S
                cost_s = self.data.CS
                mask_s = solution_copy.Oc.toarray()[0]
                inactive_s = np.where(mask_s == 0)[0]
                active_s = np.where(mask_s == 1)[0]
                if inactive_s.size and active_s.size:
                    j_s = inactive_s[np.argmin(cost_s[0, inactive_s])]
                    k_s = active_s[np.argmax(cost_s[0, active_s])]
                    solution_copy.Oces[0, j_s], solution_copy.Oces[0, k_s] = 1, 0
                # E -> N2
                cost_n2 = self.data.CN
                mask_n2 = solution_copy.O.toarray()[0]
                inactive_n2 = np.where(mask_n2 == 0)[0]
                active_n2 = np.where(mask_n2 == 1)[0]
                if inactive_n2.size and active_n2.size:
                    j_n2 = inactive_n2[np.argmin(cost_n2[0, inactive_n2])]
                    k_n2 = active_n2[np.argmax(cost_n2[0, active_n2])]
                    solution_copy.Oen2[0, j_n2], solution_copy.Oen2[0, k_n2] = 1, 0

            elif chromosome_attr == 'S4':  # Processing center -> pistachio factories
                cost = self.data.CK
                inactive = np.where(row_mask == 0)[0]
                active = np.where(row_mask == 1)[0]
                if not inactive.size or not active.size:
                    continue
                j = inactive[np.argmin(cost[0, inactive])]
                k = active[np.argmax(cost[0, active])]
                new_chrom = swap_bits(chromosome, k, j)
                setattr(solution_copy, chromosome_attr, new_chrom)

            elif chromosome_attr == 'S5':  # Processing center -> oil extraction center
                cost = self.data.CE
                inactive = np.where(row_mask == 0)[0]
                active = np.where(row_mask == 1)[0]
                if not inactive.size or not active.size:
                    continue
                j = inactive[np.argmin(cost[0, inactive])]
                k = active[np.argmax(cost[0, active])]
                new_chrom = swap_bits(chromosome, k, j)
                setattr(solution_copy, chromosome_attr, new_chrom)

            elif chromosome_attr == 'S6':  # Pistachio producers -> processing centers
                cost = self.data.CX
                inactive = np.where(row_mask == 0)[0]
                active = np.where(row_mask == 1)[0]
                if not inactive.size or not active.size:
                    continue
                j = inactive[np.argmin(cost[0, inactive])]
                k = active[np.argmax(cost[0, active])]
                new_chrom = swap_bits(chromosome, k, j)
                setattr(solution_copy, chromosome_attr, new_chrom)

            elif chromosome_attr == 'S7':  # Composting centers -> composting consumers
                cost = self.data.Cd
                inactive = np.where(row_mask == 0)[0]
                active = np.where(row_mask == 1)[0]
                if not inactive.size or not active.size:
                    continue
                j = inactive[np.argmin(cost[0, inactive])]
                k = active[np.argmax(cost[0, active])]
                new_chrom = swap_bits(chromosome, k, j)
                setattr(solution_copy, chromosome_attr, new_chrom)

            elif chromosome_attr == 'S8':  # Oil extraction centers -> composting centers
                cost = self.data.CQ
                inactive = np.where(row_mask == 0)[0]
                active = np.where(row_mask == 1)[0]
                if not inactive.size or not active.size:
                    continue
                j = inactive[np.argmin(cost[0, inactive])]
                k = active[np.argmax(cost[0, active])]
                new_chrom = swap_bits(chromosome, k, j)
                setattr(solution_copy, chromosome_attr, new_chrom)

        return solution_copy
