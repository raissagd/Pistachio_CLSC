from abc import ABC, abstractmethod
from Solution import Solution
import numpy as np

class Algorithm(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def solve(self, data):
        pass
    
class IteratedLocalSearch(Algorithm):
    def __init__(self, operators, max_iter):
        self.operators = operators # Operators for generating neighbors
        self.max_iter = max_iter # Maximum number of iterations
    
    def localSearch(self, solution, data):
        failure_counter = 0
        while True:
            neighbors = []
            Fx_neighbors = []
            
            for n in range(len(self.operators)):
                neighbor = self.operators[n].applyChange(solution) # Generate a neighbor solution (apply an operator to the current solution)
                neighbor.evaluate(data) # Evaluate the neighbor solution
                neighbors.append(neighbor) # Store the neighbor solution
                Fx_neighbors.append(neighbor.FX) # Store the fitness value of the neighbor solution
                
            best_neighbor_index = np.argmin(Fx_neighbors) 
            best_neighbor = neighbors[best_neighbor_index]
            
            # Update current solution if the best neighbor is better
            if Fx_neighbors[best_neighbor_index] < solution.FX:
                solution = best_neighbor
                failure_counter = 0
            else:
                failure_counter += 1
                if failure_counter == 5:  # If 5 consecutive failures occur, break the loop
                    break
        
        return solution

    def perturbation(self, solution, data):
        for n in range(len(self.operators)):
            solution = self.operators[n].applyChange(solution)
        solution.evaluate(data)
        
        return solution

    def solve(self, data):
        """
        Algoritmo Pesquisa Local Iterativa
            s <- Gera()
            s2 <- PesquisaLocal(s)

            repita
                s <- Perturba(s2, memória)
                s3 <- PesquisaLocal(s)
                s2 <- Aceita (s2, s3, memória)
            até condição de paragem ser verdadeira
        """ 
        solution = Solution()
        solution.generateChromosome(data)
        solution.evaluate(data)
        print(f"Initial FX: {solution.FX}")
        
        solution = self.localSearch(solution, data) # Local search on the initial solution
        
        for n in range(self.max_iter):
            perturbed_solution = self.perturbation(solution, data) # Perturbation of previous local search solution
            candidate = self.localSearch(perturbed_solution, data) # Local search on the perturbed solution
            
            if candidate.FX < solution.FX:
                solution = candidate
        
        print(f"Final solution: {solution.FX}")
        return solution