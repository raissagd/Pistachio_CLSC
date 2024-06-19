import sys
sys.path.append(r'C:\Users\Lenovo\Documents\IC')
from abc import ABC, abstractmethod
from Classes.Solution import Solution
import numpy as np
import gurobipy as grb
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
    
    def __init__(self, operators, max_eval, initialization):
        self.operators = operators # Operators for generating neighbors
        self.max_eval = max_eval # Maximum number of iterations
        self.n_eval = 1 # Number of evaluations
        self.initializaton = initialization # Initialization method
        self.FX_history = [] # List to store all FX values for plotting
    
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
        if(self.initializaton == 0):
            solution.generateChromosomeDeterministic(data)
        else:
            solution.generateChromosomeStochastic(data)
            
        solution.evaluate(data)
        print(f"Initial FX: {solution.FX}")
        operator_index = 0
        number_of_neighbors = 15 
        
        # Neighborhood change
        while True:
            perturbed_solution = self.perturbation(solution, data, operator_index) # Shake the current solution
            new_solution = self.best_improvement(perturbed_solution, data, operator_index, number_of_neighbors) # Local search on the perturbed solution
            self.FX_history.append(new_solution.FX)

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
    
class ExactAlgorithm(Algorithm):
    def __init__(self):
        pass
    
    def solve(self, data):
        # Criação do modelo
        modelo = grb.Model(
            """Otimização de rede de cadeia de abastecimento de pistache com realimentação"""
        )
        
        # Variáveis de decisão positivas: fluxos de produtos
        X = modelo.addVars(int(data.I), int(data.J), vtype=grb.GRB.CONTINUOUS, name="X", lb=0.)
        Go = modelo.addVars(int(data.J), int(data.K), vtype=grb.GRB.CONTINUOUS, name="Go", lb=0.)
        Gr = modelo.addVars(int(data.J), int(data.E), vtype=grb.GRB.CONTINUOUS, name="Gr", lb=0.)
        Gw = modelo.addVars(int(data.J), int(data.Q), vtype=grb.GRB.CONTINUOUS, name="Gw", lb=0.)
        O = modelo.addVars(int(data.E), int(data.N2), vtype=grb.GRB.CONTINUOUS, name="O", lb=0.)
        Oc = modelo.addVars(int(data.E), int(data.S), vtype=grb.GRB.CONTINUOUS, name="Oc", lb=0.)
        Ow = modelo.addVars(int(data.E), int(data.Q), vtype=grb.GRB.CONTINUOUS, name="Ow", lb=0.)
        L = modelo.addVars(int(data.S), int(data.N3), vtype=grb.GRB.CONTINUOUS, name="L", lb=0.)
        P = modelo.addVars(int(data.K), int(data.N1), vtype=grb.GRB.CONTINUOUS, name="P", lb=0.)
        D = modelo.addVars(int(data.Q), int(data.M), vtype=grb.GRB.CONTINUOUS, name="D", lb=0.)

        # Variáveis binárias: indicadores de ativação
        U = modelo.addVars(int(data.J), vtype=grb.GRB.BINARY, name="U")
        Y = modelo.addVars(int(data.Q), vtype=grb.GRB.BINARY, name="Y")
        W = modelo.addVars(int(data.K), vtype=grb.GRB.BINARY, name="W")
        R = modelo.addVars(int(data.E), vtype=grb.GRB.BINARY, name="R")
        V = modelo.addVars(int(data.S), vtype=grb.GRB.BINARY, name="V")
                
        # Custo de abertura de instalações
        z1 = (grb.quicksum(data.Fu[j] * U[j] for j in range(int(data.J)))
            + grb.quicksum(data.Fy[q] * Y[q] for q in range(int(data.Q)))
            + grb.quicksum(data.Fw[k] * W[k] for k in range(int(data.K)))
            + grb.quicksum(data.Fr[e] * R[e] for e in range(int(data.E)))
            + grb.quicksum(data.Fv[s] * V[s] for s in range(int(data.S))))

        # Custo de produção
        z2 = (grb.quicksum(data.CI[i] * X[i,j] for i in range(int(data.I)) for j in range(int(data.J)))
            + grb.quicksum(data.Cu1[j] * Go[j,k] for j in range(int(data.J)) for k in range(int(data.K)))
            + grb.quicksum(data.Cu2[j] * Gr[j,e] for j in range(int(data.J)) for e in range(int(data.E)))
            + grb.quicksum(data.Cy[q] * D[q,m] for q in range(int(data.Q)) for m in range(int(data.M)))
            + grb.quicksum(data.Cw[k] * P[k,n1] for k in range(int(data.K)) for n1 in range(int(data.N1)))
            + grb.quicksum(data.Cr[e] * O[e,n2] for e in range(int(data.E)) for n2 in range(int(data.N2)))
            + grb.quicksum(data.Cr[e] * Oc[e,s] for e in range(int(data.E)) for s in range(int(data.S)))
            + grb.quicksum(data.Cv[s] * L[s,n3] for s in range(int(data.S)) for n3 in range(int(data.N3))))

        # Custos de transporte
        z3 = (grb.quicksum(data.CX[i,j] * X[i,j] for i in range(int(data.I)) for j in range(int(data.J)))
            + grb.quicksum(data.CK[j,k] * Go[j,k] for j in range(int(data.J)) for k in range(int(data.K)))
            + grb.quicksum(data.CE[j,e] * Gr[j,e] for j in range(int(data.J)) for e in range(int(data.E)))
            + grb.quicksum(data.CJ[j,q] * Gw[j,q] for j in range(int(data.J)) for q in range(int(data.Q)))
            + grb.quicksum(data.CS[e,s] * Oc[e,s] for e in range(int(data.E)) for s in range(int(data.S)))
            + grb.quicksum(data.CN[e,n2] * O[e,n2] for e in range(int(data.E)) for n2 in range(int(data.N2)))
            + grb.quicksum(data.CQ[e,q] * Ow[e,q] for e in range(int(data.E)) for q in range(int(data.Q)))
            + grb.quicksum(data.Cl[s,n3] * L[s,n3] for s in range(int(data.S)) for n3 in range(int(data.N3)))
            + grb.quicksum(data.Cp[k,n1] * P[k,n1] for k in range(int(data.K)) for n1 in range(int(data.N1)))
            + grb.quicksum(data.Cd[q,m] * D[q,m] for q in range(int(data.Q)) for m in range(int(data.M))))

        
        # Definindo a função objetivo
        modelo.setObjective(z1 + z2 + z3, grb.GRB.MINIMIZE)

        # Restrição de capacidade
        modelo.addConstrs(
            (grb.quicksum(X[i,j] for j in range(int(data.J))) <= data.Cpa[i] for i in range(int(data.I))), 
            name="Eq.(4)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(X[i,j] for i in range(int(data.I))) <= data.Cpu[j] * U[j] for j in range(int(data.J))), 
            name="Eq.(5)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(Ow[e,q] for e in range(int(data.E))) + grb.quicksum(Gw[j,q] for j in range(int(data.J))) 
            <= data.Cpy[q] * Y[q] for q in range(int(data.Q))), name="Eq.(6)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(Go[j,k] for j in range(int(data.J))) <= data.Cpw[k] * W[k] for k in range(int(data.K))),
            name="Eq.(7)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(Gr[j,e] for j in range(int(data.J))) <= data.Cpr[e] * R[e] for e in range(int(data.E))), 
            name="Eq.(8)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(Oc[e,s] for e in range(int(data.E))) <= data.Cpv[s] * V[s] for s in range(int(data.S))),
            name="Eq.(9)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(Go[j,k] for k in range(int(data.K))) + grb.quicksum(Gr[j,e] for e in range(int(data.E))) + grb.quicksum(Gw[j,q] for q in range(int(data.Q)))
            <= grb.quicksum(X[i,j] for i in range(int(data.I))) for j in range(int(data.J))),
            name="Eq.(10)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(Go[j,k] for k in range(int(data.K)))
            == (1 - data.beta)  * data.theta[0] * grb.quicksum(X[i,j] for i in range(int(data.I))) for j in range(int(data.J))),
            name="Eq.(11)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(Gr[j,e] for e in range(int(data.E)))
            == (1 - data.beta) * data.theta[1] * grb.quicksum(X[i,j] for i in range(int(data.I))) for j in range(int(data.J))),
            name="Eq.(12)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(Gw[j,q] for q in range(int(data.Q)))
            == data.theta[2] * grb.quicksum(X[i,j] for i in range(int(data.I))) for j in range(int(data.J))), 
            name="Eq.(13)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(P[k,n1] for n1 in range(int(data.N1)))
            <= data.gammak * grb.quicksum(Go[j,k] for j in range(int(data.J))) for k in range(int(data.K))),
            name="Eq.(14)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(O[e,n2] for n2 in range(int(data.N2))) + grb.quicksum(Oc[e,s] for s in range(int(data.S))) 
            <= (1- data.lamb) * grb.quicksum(Gr[j,e] for j in range(int(data.J))) for e in range(int(data.E))), 
            name="Eq.(15)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(Ow[e,q] for q in range(int(data.Q)))
            <= data.lamb * grb.quicksum(Gr[j,e] for j in range(int(data.J))) for e in range(int(data.E))), 
            name="Eq.(16)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(L[s,n3] for n3 in range(int(data.N3))) 
            <= data.gammas * grb.quicksum(Oc[e,s] for e in range(int(data.E))) for s in range(int(data.S))),
            name="Eq.(17)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(D[q,m] for m in range(int(data.M)))
            <= data.gammaq*(grb.quicksum(Gw[j,q] for j in range(int(data.J))) + grb.quicksum(Ow[e,q] for e in range(int(data.E)))) for q in range(int(data.Q))), 
            name="Eq.(18)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(P[k,n1] for k in range(int(data.K))) >= data.Dp[n1] for n1 in range(int(data.N1))), 
            name="Eq.(19)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(O[e,n2] for e in range(int(data.E))) >= data.Du[n2] for n2 in range(int(data.N2))), 
            name="Eq.(20)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(L[s,n3] for s in range(int(data.S))) >= data.Ds[n3] for n3 in range(int(data.N3))), 
            name="Eq.(21)"
        )
        
        modelo.addConstrs(
            (grb.quicksum(D[q,m] for q in range(int(data.Q))) >= data.Dc[m] for m in range(int(data.M))),
            name="Eq.(22)"
        )

        # Resolvendo o modelo
        modelo.optimize()
        
        # Retornando o valor da função objetivo
        return modelo.objVal
                   
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
    
class GeneticAlgorithm(Algorithm):
    def __init__(self, population_size, crossover_rate, mutation_rate, max_generations, initialization):
        self.population_size = population_size  # Size of the population
        self.crossover_rate = crossover_rate  # Crossover rate
        self.mutation_rate = mutation_rate  # Mutation rate
        self.max_generations = max_generations  # Maximum number of generations
        self.initialization = initialization  # Initialization method for the population
        
    def initialize_population(self, data):
        # Initialize the population with random solutions
        population = []
        for _ in range(self.population_size):
            solution = Solution()
            if self.initialization == 0:
                # Generate chromosome deterministically
                solution.generateChromosomeDeterministic(data)
            else:
                # Generate chromosome stochastically
                solution.generateChromosomeStochastic(data)
            # Evaluate the solution
            solution.evaluate(data)
            # Add the solution to the population
            population.append(solution)
        return population
    
    def select_parents(self, population):
        # Select two parents from the population based on their fitness (FX)
        fitness_values = np.array([1/sol.FX for sol in population])
        probabilities = fitness_values / np.sum(fitness_values)
        # Roulette wheel selection
        parents = np.random.choice(population, size=2, p=probabilities, replace=False)
        return parents
    
    def crossover(self, parent1, parent2):
        # Perform crossover between two parents to produce two children
        child1, child2 = Solution(), Solution()
        crossover_point = np.random.randint(1, 8)  # Crossover point
        
        for i in range(1, 9):
            if i <= crossover_point:
                # Assign segments from parents to children
                setattr(child1, f"S{i}", getattr(parent1, f"S{i}").copy())
                setattr(child2, f"S{i}", getattr(parent2, f"S{i}").copy())
            else:
                setattr(child1, f"S{i}", getattr(parent2, f"S{i}").copy())
                setattr(child2, f"S{i}", getattr(parent1, f"S{i}").copy())
                
        return child1, child2
    
    def mutate(self, solution):
        # Perform mutation on a segment of the solution's chromosome
        segment = np.random.randint(1, 9)  # Select a random segment
        chromosome = getattr(solution, f"S{segment}").copy()
        # Select two random positions in the segment to swap
        i, j = np.random.randint(0, len(chromosome), size=2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
        # Update the solution's segment with the mutated chromosome
        setattr(solution, f"S{segment}", chromosome)
    
    def solve(self, data):
        # Solve the problem using the genetic algorithm
        population = self.initialize_population(data)
        
        for generation in range(self.max_generations):
            new_population = []
            
            while len(new_population) < self.population_size:
                # Select two parents from the current population
                parent1, parent2 = self.select_parents(population)
                
                # Perform crossover based on the crossover rate
                if np.random.rand() < self.crossover_rate:
                    child1, child2 = self.crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2
                
                # Perform mutation based on the mutation rate
                if np.random.rand() < self.mutation_rate:
                    self.mutate(child1)
                if np.random.rand() < self.mutation_rate:
                    self.mutate(child2)
                
                # Evaluate the new solutions
                child1.evaluate(data)
                child2.evaluate(data)
                
                # Add the new solutions to the new population
                new_population.extend([child1, child2])
            
            # Update the population, keeping only the best individuals
            population = sorted(new_population, key=lambda sol: sol.FX)[:self.population_size]
            best_solution = population[0]
            #print(f"Generation {generation}: Best FX = {best_solution.FX}")
        
        return best_solution  # Return the best solution found