import sys
sys.path.insert(0, 'Classes/')
from Problem import loadInstance
from Persistence import PersistMultipleSolutions
from Execute import RunMultipleMethodsMultipleTimes
from Algorithm import IteratedLocalSearch
from Neighborhood import Swap, InactiveActiveSwap

# Experiment parameters
experiment_name = "test_num_evals"
instance = 400

# Load problem instance
problem = loadInstance("data_" + str(instance), quiet=True)
print(f"Number of variables: {problem.num_var_priority}")

# Set maximum evaluations
num_evals = problem.num_var_priority

# Initialize the Iterated Local Search algorithm
ils = IteratedLocalSearch(InactiveActiveSwap(1), max_eval=num_evals, initialization=0,
                          number_neighbors=20, noimprovement_limit=10)

# Run the algorithm
solution = ils.solve(problem, quiet=False)