from abc import ABC, abstractmethod
from Solution import Solution
import numpy as np
import random

class Algorithm(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def solve(self, data):
        pass
    
class VariableNeighborhoodSearch(Algorithm):
    """
    Function VNS (x, kmax)
        1:    k ← 1
        2:    repeat
        3:       x' ← Shake(x, k)                     // Perturbation of the solution
        4:       x'' ← BestImprovement(x')           // Local search
        5:       x ← NeighbourhoodChange(x, x'', k) // If x'' is better, change the neighborhood. Repeat the process
        6:    until k = kmax
    """
    
    def __init__(self, operators, max_eval):
        self.operators = operators # Operators for generating neighbors
        self.max_eval = max_eval # Maximum number of iterations
        self.n_eval = 1 # Number of evaluations
    
    def best_improvement(self, solution, data, operator_index, number_of_neighbors):
        failure_counter = 0
        while True:
            neighbors = [] # List to store the neighbor solutions
            Fx_neighbors = [] # List to store the fitness values of the neighbor solutions
            
            for _ in range(number_of_neighbors):
                neighbor = self.operators[operator_index].applyChange(solution) # Generate a neighbor solution (apply an operator to the current solution)
                neighbor.evaluate(data) # Evaluate the neighbor solution
                neighbors.append(neighbor) # Store it
                Fx_neighbors.append(neighbor.FX) # Store its fitness value
                
            best_neighbor_index = np.argmin(Fx_neighbors) 
            best_neighbor = neighbors[best_neighbor_index] # Select the best neighbor
            
            # Update the current solution if the best neighbor is better
            if Fx_neighbors[best_neighbor_index] < solution.FX:
                solution = best_neighbor
                failure_counter = 0
            else:
                failure_counter += 1
                if failure_counter == 5:  # If 5 consecutive failures occur, break the loop
                    break
                
        self.n_eval += 1
        return solution

    def perturbation(self, solution, data, operator_index):
        operator = self.operators[operator_index] # Select the operator for perturbation
        
        solution = operator.applyChange(solution) # Generate a perturbed solution
         
        solution.evaluate(data) # Evaluate the perturbed solution
        
        self.n_eval += 1
        return solution
        
    def solve(self, data):
        solution = Solution() # Create a new solution
        solution.generateChromosome(data)
        solution.evaluate(data)
        print(f"Initial FX: {solution.FX}")
        operator_index = 0
        number_of_neighbors = 15 
        
        # Neighborhood change
        while True:
            perturbed_solution = self.perturbation(solution, data, operator_index) # Shake the current solution
            new_solution = self.best_improvement(perturbed_solution, data, operator_index, number_of_neighbors) # Local search on the perturbed solution
            
            if new_solution.FX < solution.FX:
                # If the new solution is better, update the current solution and repeat the process
                solution = new_solution
                operator_index = 0
            elif self.n_eval >= self.max_eval:
                # If the maximum number of evaluations is reached,
                break
            elif operator_index == len(self.operators) - 1:
                # If all operators have been tested,
                break
            else:
                # If the new solution is not better, try the next operator
                operator_index += 1
            
        print(f"Final solution: {solution.FX}")
        return solution
    
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