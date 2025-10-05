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
                solution_copy
            )
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
    Operador que identifica arestas inativas de alto potencial de economia
    e promove tanto a fonte quanto o cliente envolvidos, com base em critérios heurísticos.
    """
    def __init__(self, N, data, top_k=10):
        super().__init__(N)
        self.data = data
        self.top_k = top_k

    def applyChange(self, solution):
        sol = copy.deepcopy(solution)

        for _ in range(self.N):
            attr, chrom = self.selectRandomChromosome(sol)

            # Seleção das matrizes de custo e fluxo
            if attr == 'S1':
                cost = self.data.Cp
                flow = sol.P.toarray()
            elif attr == 'S2':
                cost = self.data.Cl
                flow = sol.L.toarray()
            elif attr == 'S3':
                cost = np.hstack((self.data.CN, self.data.CS))
                flow = np.hstack((sol.O.toarray(), sol.Oc.toarray()))
            elif attr == 'S4':
                cost = self.data.CK
                flow = sol.Go.toarray()
            elif attr == 'S5':
                cost = self.data.CE
                flow = sol.Gr.toarray()
            elif attr == 'S6':
                cost = self.data.CX
                flow = sol.X.toarray()
            elif attr == 'S7':
                cost = self.data.Cd
                flow = sol.D.toarray()
            elif attr == 'S8':
                cost = self.data.CQ
                flow = sol.Ow.toarray()
            else:
                continue

            K, J = cost.shape

            ativa   = np.argwhere(flow > 0)
            inativa = np.argwhere(flow == 0)

            if inativa.size == 0:
                continue

            # Calcula os custos das arestas inativas
            custos_in = np.array([cost[k, j] for (k, j) in inativa])
            top_idxs  = np.argsort(custos_in)[:self.top_k]  # top-k arestas inativas mais baratas

            melhores = []
            for idx in top_idxs:
                k, j = inativa[idx]

                # Verifica se o cliente j já recebe de outra fonte
                fontes_ativas_para_j = ativa[ativa[:, 1] == j]
                if len(fontes_ativas_para_j) == 0:
                    continue

                # Custo atual médio que o cliente j está recebendo
                custo_atual = np.mean([cost[ka, j] for (ka, _) in fontes_ativas_para_j])
                custo_novo  = cost[k, j]

                # Se a nova aresta é melhor, registra
                if custo_novo < custo_atual:
                    ganho_estimado = custo_atual - custo_novo
                    melhores.append((ganho_estimado, k, j))

            if not melhores:
                continue

            # Escolhe o melhor par (ganho mais alto)
            _, k_chp, j_chp = max(melhores)

            # Atualiza prioridade no cromossomo (cliente e fonte)
            chrom_old = chrom.copy()
            chrom_new = chrom_old.copy()

            p_old_src = chrom_old[k_chp]
            p_old_cli = chrom_old[K + j_chp]
            p_max     = chrom_old.max()

            # Ajusta prioridades: cliente e fonte vão para o topo
            chrom_new[chrom_new > p_old_src] -= 1
            chrom_new[chrom_new > p_old_cli] -= 1
            chrom_new[k_chp]      = p_max
            chrom_new[K + j_chp]  = p_max

            setattr(sol, attr, chrom_new)

        return sol
    
class SourceCostBoost(Neighborhood):
    """
    Operador que promove uma fonte inativa com maior potencial de economia,
    baseado na média dos menores custos da linha de custo da matriz (estimativa local).
    """
    def __init__(self, N, data, top_k=5):
        super().__init__(N)
        self.data = data
        self.top_k = top_k  # número de menores custos considerados por fonte

    def applyChange(self, solution):
        sol = copy.deepcopy(solution)

        for _ in range(self.N):
            attr, chrom = self.selectRandomChromosome(sol)

            # Mapeamento das matrizes de custo e fluxos
            if attr == 'S1':
                cost = self.data.Cp
                flow = sol.P.toarray()
            elif attr == 'S2':
                cost = self.data.Cl
                flow = sol.L.toarray()
            elif attr == 'S3':
                cost = np.hstack((self.data.CN, self.data.CS))
                flow = np.hstack((sol.O.toarray(), sol.Oc.toarray()))
            elif attr == 'S4':
                cost = self.data.CK
                flow = sol.Go.toarray()
            elif attr == 'S5':
                cost = self.data.CE
                flow = sol.Gr.toarray()
            elif attr == 'S6':
                cost = self.data.CX
                flow = sol.X.toarray()
            elif attr == 'S7':
                cost = self.data.Cd
                flow = sol.D.toarray()
            elif attr == 'S8':
                cost = self.data.CQ
                flow = sol.Ow.toarray()
            else:
                continue

            K, J = cost.shape

            # Verifica fontes inativas (sem fluxo positivo)
            flow_sum_by_source = flow.sum(axis=1)
            fontes_inativas = np.where(flow_sum_by_source == 0)[0]

            if len(fontes_inativas) == 0:
                continue  # nada a boostar

            # Avalia a atratividade de cada fonte inativa
            atratividade = []
            for k in fontes_inativas:
                menores_custos = np.partition(cost[k], self.top_k)[:self.top_k]
                score = menores_custos.mean()
                atratividade.append((score, k))

            # Escolhe a mais promissora (menor score)
            _, k_melhor = min(atratividade)

            # Atualiza prioridade da fonte escolhida
            chrom_old = chrom.copy()
            chrom_new = chrom_old.copy()

            p_old = chrom_old[k_melhor]
            p_max = chrom_old.max()

            mask = chrom_new > p_old
            chrom_new[mask] -= 1
            chrom_new[k_melhor] = p_max

            setattr(sol, attr, chrom_new)

        return sol

class InactiveActiveSwap(Neighborhood):
    """
    Swaps priorities between an active node and an inactive node.
    The active node gets lower priority and the inactive node gets higher priority.
    """
    
    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            # Select a random chromosome
            chromosome_attr, chromosome = self.selectRandomChromosome(solution_copy)
            
            # Get the corresponding active nodes array
            active_attr = chromosome_attr.replace('S', 'A')  # S1 -> A1, S2 -> A2, etc.
            active_nodes = getattr(solution_copy, active_attr)
            
            # Skip if active_nodes is None (hasn't been computed yet)
            if active_nodes is None:
                continue
                
            # Find active and inactive nodes
            active_indices = np.where(active_nodes == 1)[0]
            inactive_indices = np.where(active_nodes == 0)[0]
            
            # Skip if there are no active or inactive nodes
            if len(active_indices) == 0 or len(inactive_indices) == 0:
                continue
            
            # Randomly select one active and one inactive node
            i = np.random.choice(active_indices)  # Active node index
            j = np.random.choice(inactive_indices)  # Inactive node index
            
            # Swap the priorities between active and inactive nodes
            chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
            
            # Update the solution with the modified chromosome
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy

class InactiveActiveReversion(Neighborhood):
    """
    Reverses a segment that includes both an active and inactive node,
    effectively swapping their relative positions.
    """
    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(solution_copy)
            active_attr = chromosome_attr.replace('S', 'A')
            active_nodes = getattr(solution_copy, active_attr)
            
            if active_nodes is None:
                continue
                
            active_indices = np.where(active_nodes == 1)[0]
            inactive_indices = np.where(active_nodes == 0)[0]
            
            if len(active_indices) == 0 or len(inactive_indices) == 0:
                continue
            
            i = np.random.choice(active_indices)
            j = np.random.choice(inactive_indices)
            
            # Garante que revertemos do menor para o maior índice
            start = min(i, j)
            end = max(i, j) + 1
            chromosome[start:end] = chromosome[start:end][::-1]

            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class InactiveActiveInsertion(Neighborhood):
    """
    Extracts an inactive node and inserts it immediately after an active node,
    giving it higher priority.
    """
    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(solution_copy)
            active_attr = chromosome_attr.replace('S', 'A')
            active_nodes = getattr(solution_copy, active_attr)
            
            if active_nodes is None:
                continue
                
            active_indices = np.where(active_nodes == 1)[0]
            inactive_indices = np.where(active_nodes == 0)[0]
            
            if len(active_indices) == 0 or len(inactive_indices) == 0:
                continue
            
            i = np.random.choice(active_indices)  # Ativo (posição alvo)
            j = np.random.choice(inactive_indices)  # Inativo (será movido)
            
            # Extrai o valor do nó inativo
            unit_to_insert = chromosome[j]
            
            if i < j:
                # Move elementos para a direita
                for k in range(j, i + 1, -1):
                    chromosome[k] = chromosome[k - 1]
                # Insere logo após i
                chromosome[i + 1] = unit_to_insert
            else:  # i > j
                # Move elementos para a esquerda
                for k in range(j, i):
                    chromosome[k] = chromosome[k + 1]
                # Insere logo após a nova posição de i
                chromosome[i] = unit_to_insert

            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class InactiveActiveSlide(Neighborhood):
    """
    Slides an inactive node to the position of an active node,
    effectively promoting the inactive node.
    """
    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(solution_copy)
            active_attr = chromosome_attr.replace('S', 'A')
            active_nodes = getattr(solution_copy, active_attr)
            
            if active_nodes is None:
                continue
                
            active_indices = np.where(active_nodes == 1)[0]
            inactive_indices = np.where(active_nodes == 0)[0]
            
            if len(active_indices) == 0 or len(inactive_indices) == 0:
                continue
            
            i = np.random.choice(inactive_indices)  # Inativo (será movido)
            j = np.random.choice(active_indices)    # Ativo (posição alvo)
            
            unit_to_move = chromosome[i]
            
            if i < j:
                # Desloca elementos para a esquerda
                for k in range(i, j):
                    chromosome[k] = chromosome[k + 1]
                chromosome[j] = unit_to_move
            else:  # i > j
                # Desloca elementos para a direita
                for k in range(i, j, -1):
                    chromosome[k] = chromosome[k - 1]
                chromosome[j] = unit_to_move

            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy
    
class InactiveBoost(Neighborhood):
    """
    Pega um nó inativo e coloca diretamente no TOPO da prioridade.
    """
    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)
        
        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(solution_copy)
            active_attr = chromosome_attr.replace('S', 'A')
            active_nodes = getattr(solution_copy, active_attr)
            
            if active_nodes is None:
                continue
            
            inactive_indices = np.where(active_nodes == 0)[0]
            if len(inactive_indices) == 0:
                continue
            
            # Pega um inativo aleatório
            i = np.random.choice(inactive_indices)
            
            # Coloca no topo (maior prioridade)
            max_priority = chromosome.max()
            chromosome[chromosome > chromosome[i]] -= 1
            chromosome[i] = max_priority + 1
            
            setattr(solution_copy, chromosome_attr, chromosome)
        
        return solution_copy
    

class InactiveActiveETN(Neighborhood):
    """
    Exchange with Nearest Active (IAETN):
    Selects an inactive node and swaps it with its nearest active neighbor.
    This is a more conservative, localized version of InactiveActiveSwap.
    """
    
    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(solution_copy)
            active_attr = chromosome_attr.replace('S', 'A')
            active_nodes = getattr(solution_copy, active_attr)
            
            if active_nodes is None:
                continue
                
            active_indices = np.where(active_nodes == 1)[0]
            inactive_indices = np.where(active_nodes == 0)[0]
            
            if len(active_indices) == 0 or len(inactive_indices) == 0:
                continue
            
            # Seleciona um nó inativo aleatório
            i = np.random.choice(inactive_indices)
            
            # Encontra o vizinho ativo mais próximo
            distances_to_actives = np.abs(active_indices - i)
            nearest_active_idx = active_indices[np.argmin(distances_to_actives)]
            
            # Troca o inativo com seu vizinho ativo mais próximo
            chromosome[i], chromosome[nearest_active_idx] = \
                chromosome[nearest_active_idx], chromosome[i]
            
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy


class MultiInactiveBoost(Neighborhood):
    """
    Multi-Inactive Boost:
    Promotes multiple inactive nodes (2-5) simultaneously to high priority positions.
    More disruptive than single InactiveBoost, useful for escaping local optima.
    """
    
    def __init__(self, N, min_boost=2, max_boost=5):
        super().__init__(N)
        self.min_boost = min_boost  # Mínimo de inativos a promover
        self.max_boost = max_boost  # Máximo de inativos a promover
    
    def applyChange(self, solution):
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            chromosome_attr, chromosome = self.selectRandomChromosome(solution_copy)
            active_attr = chromosome_attr.replace('S', 'A')
            active_nodes = getattr(solution_copy, active_attr)
            
            if active_nodes is None:
                continue
                
            inactive_indices = np.where(active_nodes == 0)[0]
            
            if len(inactive_indices) == 0:
                continue
            
            # Determina quantos inativos promover
            num_to_boost = np.random.randint(
                self.min_boost, 
                min(self.max_boost, len(inactive_indices)) + 1
            )
            
            # Seleciona aleatoriamente quais inativos promover
            selected_inactives = np.random.choice(
                inactive_indices, 
                size=num_to_boost, 
                replace=False
            )
            
            # Promove todos os selecionados para o topo
            # Mantém a ordem relativa entre eles
            max_priority = chromosome.max()
            
            for idx, inactive_idx in enumerate(selected_inactives):
                old_priority = chromosome[inactive_idx]
                new_priority = max_priority + idx + 1
                
                # Ajusta as prioridades dos outros
                mask = chromosome > old_priority
                chromosome[mask] -= 1
                
                # Define a nova prioridade alta
                chromosome[inactive_idx] = new_priority
            
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy