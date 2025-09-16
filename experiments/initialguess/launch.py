"""
Initial Guess Experiment Script
This script conducts experiments to compare different initialization methods
for the Iterated Local Search (ILS) algorithm on a Pistachio CLSC problem instance.
The experiment:
- Loads a specific problem instance (configurable by instance number)
- Sets up two ILS algorithms with different initialization strategies (0 and 1)
- Both algorithms use Swap(1) neighborhood and the same evaluation budget
- Runs each algorithm 30 times to gather statistical data
- Saves results for analysis
Parameters:
    experiment_name (str): Name identifier for the experiment ("initialguess")
    instance (int): Problem instance number to test (400)
    results_path (str): Directory path where results will be saved
    num_evals (int): Maximum number of evaluations (num_variables * 100)
Output:
    Saves experimental results to the specified results path with detailed
    performance metrics for both initialization methods.
"""
import sys
sys.path.insert(0, 'Classes/')
from Problem import loadInstance
from Persistence import PersistMultipleSolutions
from Execute import RunMultipleMethodsMultipleTimes
from Algorithm import IteratedLocalSearch
from Neighborhood import Swap

# Experiment parameters
experiment_name = "initialguess"
instance = 400
results_path = f'./experiments/initialguess/results/'

# Load problem instance
problem = loadInstance("data_" + str(instance), quiet=True)
print(f"Number of variables: {problem.num_var_priority}")

# Set maximum evaluations
num_evals = problem.num_var_priority * 100

# Configure ILS algorithms with different neighborhoods
ils = [IteratedLocalSearch(Swap(1), max_eval=num_evals, initialization=0),
       IteratedLocalSearch(Swap(1), max_eval=num_evals, initialization=1)]

# Run experiments
results = RunMultipleMethodsMultipleTimes().run(data=problem, methods=ils,
                                                number_times=30, pre_save=True,
                                                filename=results_path
                                                + f"{experiment_name}_{instance}")

# Save results
PersistMultipleSolutions().save(solutions=results, 
                                filename=f"{experiment_name}_{instance}", 
                                filepath=results_path, log=False)