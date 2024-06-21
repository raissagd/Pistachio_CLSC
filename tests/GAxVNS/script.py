import sys
sys.path.append(r'C:\Users\Lenovo\Documents\IC')
from Classes.Problem import Problem
from Classes.Algorithm import GeneticAlgorithm
import numpy as np

data = Problem()
data.loadFile("data/data_10.npz")

# Genetic Algorithm parameters
population_size = 100
crossover_rate = 0.8
mutation_rate = 0.2
max_generations = 1000
initialization = 1
elite_size = int(0.05 * population_size)  # 5% of the population size

# Storage for best solutions
best_solutions = []

for i in range(30):
    ga = GeneticAlgorithm(
        population_size=population_size,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate,
        max_generations=max_generations,
        initialization=initialization,
        elite_size=elite_size
    )
    best_solution = ga.solve(data)
    best_solutions.append(best_solution.FX)
    print(f"Iteration {i+1}: Best solution found: {best_solution.FX}")

np.savez('solutions_10_GA.npz', best_solutions=best_solutions)