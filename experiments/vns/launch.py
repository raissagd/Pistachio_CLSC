"""
Variable Neighborhood Search (VNS) Experiment Launcher

This script conducts comprehensive experiments using Variable Neighborhood Search 
algorithms to solve Closed-Loop Supply Chain (CLSC) optimization problems for 
pistachio distribution networks.

The experiment evaluates four different VNS configurations, each utilizing distinct
neighborhood operator sets to explore the solution space. Each configuration is
executed 30 times to ensure statistical significance of the results.

Neighborhood Operator Sets:
    1. Basic operators: Swap, Reversion, Insertion, Slide
    2. Advanced operators: ETN, RS, SPS, SRPS  
    3. Problem-specific operators: InactiveActiveSwap, SourceDepotSwap, 
       FixedCostSwap, TransportCostSwap, SourceCostBoost
    4. Hybrid set: Swap, InactiveActiveSwap, TransportCostSwap, SourceCostBoost

Configuration:
    - Instance size: Configurable (default: 400)
    - Initial solution: Deterministic (0) or Stochastic (1)
    - Max evaluations: num_variables * 100
    - Runs per configuration: 30
    - Results saved to: ./experiments/vns/results/

Output:
    - Statistical results for each VNS configuration
    - Serialized solution objects for further analysis
    - Performance metrics and convergence data

Usage:
    Modify the 'instance' variable to test different problem sizes.
    Adjust 'initial_guess' to change the initial solution generation method.
    Results are automatically saved with timestamps for comparison.

"""

import sys
sys.path.insert(0, 'Classes/')
from Problem import loadInstance
from Persistence import PersistMultipleSolutions
from Execute import RunMultipleMethodsMultipleTimes
from Algorithm import VariableNeighborhoodSearch
from Neighborhood import *

# Experiment parameters
experiment_name = "vns"
instance = 400
results_path = f'./experiments/vns/results/'
initial_guess = 0 # 0: Deterministic, 1: Stochastic

# Load problem instance
problem = loadInstance("data_" + str(instance), quiet=True)
print(f"Number of variables: {problem.num_var_priority}")

# Set maximum evaluations
num_evals = problem.num_var_priority * 100

operators_sets = [
    [Swap(1), Reversion(1), Insertion(1), Slide(1)],
    [ETN(1), RS(1), SPS(1), SRPS(1)],
    [InactiveActiveSwap(1), SourceDepotSwap(1), FixedCostSwap(1),TransportCostSwap(1),  SourceCostBoost(1)],
    [Swap(1), InactiveActiveSwap(1), TransportCostSwap(1),  SourceCostBoost(1)]
]

# Configure VNS algorithms with different neighborhoods
vns = [VariableNeighborhoodSearch(operators_sets[0], num_evals, initial_guess),
       VariableNeighborhoodSearch(operators_sets[1], num_evals, initial_guess),
       VariableNeighborhoodSearch(operators_sets[2], num_evals, initial_guess),
       VariableNeighborhoodSearch(operators_sets[3], num_evals, initial_guess)
]

# Run experiments
results = RunMultipleMethodsMultipleTimes().run(data=problem, methods=vns,
                                                number_times=30, pre_save=True,
                                                filename=results_path
                                                + f"{experiment_name}_{instance}")

# Save results
PersistMultipleSolutions().save(solutions=results, 
                                filename=f"{experiment_name}_{instance}", 
                                filepath=results_path, log=False)