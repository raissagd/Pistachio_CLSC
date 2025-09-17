

"""
Genetic Algorithm Experiment Launcher for CLSC Optimization

This script conducts comprehensive experiments using Genetic Algorithm variants
to solve Closed-Loop Supply Chain (CLSC) optimization problems for pistachio
distribution networks. The experiment evaluates three different crossover
operators to determine their effectiveness on multi-objective optimization.

The experiment compares three GA configurations:
1. **Segment Crossover**: Traditional segment-based crossover operation
2. **Intra-Segment Crossover**: Crossover within individual chromosome segments  
3. **Hybrid Crossover**: Adaptive combination of multiple crossover strategies

Configuration Parameters:
    - Instance size: Configurable (default: 400 variables)
    - Population size: √n (square root of number of variables)
    - Maximum evaluations: num_variables × 100
    - Initial solution: Deterministic (0) or Stochastic (1)
    - Runs per configuration: 30
    - Total experiments: 90 runs (3 configs × 30 runs)

Population Sizing Strategy:
    Uses square root rule for population size calculation, providing a balance
    between solution diversity and computational efficiency. For a 400-variable
    problem, this results in a population of 20 individuals.

Crossover Operators:
    - **segment**: Standard genetic crossover between chromosome segments
    - **intra_segment**: Crossover operations within individual segments
    - **hybrid**: Combination of different crossover strategies for enhanced
      exploration and exploitation

Output:
    - Statistical performance metrics for each GA configuration
    - Convergence data and solution quality comparisons
    - Serialized results saved to ./experiments/ga/results/
    - Comparative analysis data for crossover operator effectiveness

Usage:
    Modify 'instance' variable to test different problem sizes.
    Adjust 'initial_guess' to change solution initialization method.
    Results include fitness evolution, runtime statistics, and best solutions.

"""

import sys
sys.path.insert(0, 'Classes/')
from Problem import loadInstance
from Persistence import PersistMultipleSolutions
from Execute import RunMultipleMethodsMultipleTimes
from Algorithm import GeneticAlgorithm
from numpy import sqrt

# Experiment parameters
experiment_name = "ga"
instance = 400
results_path = f'./experiments/ga/results/'
initial_guess = 0 # 0: Deterministic, 1: Stochastic

# Load problem instance
problem = loadInstance("data_" + str(instance), quiet=True)
print(f"Number of variables: {problem.num_var_priority}")

# Set maximum evaluations
num_evals = problem.num_var_priority * 100

# Calculate population size using square root rule
population_size = int(sqrt(problem.num_var_priority))

# Configure VNS algorithms with different neighborhoods
ga = [
    GeneticAlgorithm(population_size, max_eval=num_evals, crossover_type='segment'),
    GeneticAlgorithm(population_size, max_eval=num_evals, crossover_type='intra_segment'),
    GeneticAlgorithm(population_size, max_eval=num_evals, crossover_type='hybrid')
]

# Run experiments
results = RunMultipleMethodsMultipleTimes().run(data=problem, methods=ga,
                                                number_times=30, pre_save=True,
                                                filename=results_path
                                                + f"{experiment_name}_{instance}")

# Save results
PersistMultipleSolutions().save(solutions=results, 
                                filename=f"{experiment_name}_{instance}", 
                                filepath=results_path, log=False)