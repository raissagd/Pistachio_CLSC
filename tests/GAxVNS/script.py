import sys
sys.path.append(r'C:\Users\Lenovo\Documents\IC')
from Classes.Problem import Problem
from Classes.Algorithm import GeneticAlgorithm
import numpy as np

data = Problem()
data.loadFile("data/data_100.npz")

# Genetic Algorithm parameters
population_size = 100
crossover_rate = 0.8
mutation_rate = 0.2
max_generations = 500
initialization = 1

# Storage for best solutions
best_solutions = []

for i in range(30):
    ga = GeneticAlgorithm(
        population_size=population_size,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate,
        max_generations=max_generations,
        initialization=initialization
    )
    best_solution = ga.solve(data)
    best_solutions.append(best_solution.FX)
    print(f"Iteration {i+1}: Best solution found: {best_solution.FX}")

np.savez('solutions_100_GA.npz', best_solutions=best_solutions)