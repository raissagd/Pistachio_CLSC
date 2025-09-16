"""
Iterated Local Search (ILS) Experiment Launcher
This script runs experiments using the Iterated Local Search algorithm with different
neighborhood operators on a specific problem instance.
The script performs the following operations:
1. Loads a problem instance from the specified data file
2. Configures four ILS algorithms with different neighborhood operators:
    - Swap neighborhood
    - Reversion neighborhood  
    - InactiveActiveSwap neighborhood
    - SourceDepotSwap neighborhood
3. Runs each algorithm 30 times on the problem instance
4. Saves the results to files in the specified results directory
Variables:
     instance (int): Problem instance number (400)
     problem: Loaded problem instance object
     num_evals (int): Maximum number of evaluations per run (problem.num_var_priority * 100)
     results_path (str): Directory path for saving results
     ils (list): List of ILS algorithm instances with different neighborhoods
     results: Experimental results from running all methods multiple times
Output:
     Results are saved as files in the './experiments/ils/results/' directory
     with filename pattern 'ils_{instance}'
"""
import sys
sys.path.insert(0, 'Classes/')
from Problem import loadInstance
from Persistence import PersistMultipleSolutions
from Execute import RunMultipleMethodsMultipleTimes
from Algorithm import IteratedLocalSearch
from Neighborhood import Swap, Reversion, InactiveActiveSwap, SourceDepotSwap

# Experiment parameters
experiment_name = "ils"
instance = 400
results_path = f'./experiments/ils/results/'
initialization_method = 0  # 0 for deterministic, 1 for stochastic

# Load problem instance
problem = loadInstance("data_" + str(instance), quiet=True)
print(f"Number of variables: {problem.num_var_priority}")

# Set maximum evaluations
num_evals = problem.num_var_priority * 100

# Configure ILS algorithms with different neighborhoods
ils = [IteratedLocalSearch(Swap(1), max_eval=num_evals, 
                           initialization=initialization_method),
       IteratedLocalSearch(Reversion(1), max_eval=num_evals, 
                           initialization=initialization_method),
       IteratedLocalSearch(InactiveActiveSwap(1), max_eval=num_evals, 
                           initialization=initialization_method),
       IteratedLocalSearch(SourceDepotSwap(1, problem), max_eval=num_evals, 
                           initialization=initialization_method)]

# Run experiments
results = RunMultipleMethodsMultipleTimes().run(data=problem, methods=ils,
                                                number_times=30, pre_save=True,
                                                filename=results_path
                                                + f"{experiment_name}_{instance}")

# Save results
PersistMultipleSolutions().save(solutions=results,
                                filename=f"{experiment_name}_{instance}", 
                                filepath=results_path, log=False)
