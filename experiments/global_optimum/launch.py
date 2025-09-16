"""
Global Optimum Solver Script
This script solves optimization problems for multiple instance sizes using an exact algorithm
to find global optimal solutions. It processes a series of predefined problem instances,
applies an exact solving algorithm with no time limit, and persists the optimal solutions
to disk for later analysis.
The script iterates through problem instances of varying sizes (10, 30, 100, 200, 400, 800, 1600)
and for each instance:
1. Loads the problem data from the corresponding data file
2. Initializes an exact algorithm solver with unlimited time
3. Computes the global optimal solution
4. Saves the solution to the specified results directory
Files:
    - Input: Problem instance files in format "data_{size}"
    - Output: Solution files saved as "globopt_{size}" in ./experiments/global_optimum/solutions/
Dependencies:
    - Problem: For loading problem instances
    - Algorithm: For the ExactAlgorithm solver
    - Persistence: For saving solutions to disk
Note: This script is designed for computational experiments where finding the true global
optimum is required, typically for benchmarking or validation purposes.
"""
import sys
sys.path.insert(0, 'Classes/')
from Problem import loadInstance
from Persistence import PersistSingleSolution
from Algorithm import ExactAlgorithm

# Define the list of problem instance sizes to solve
instances = [400, 800, 1600] # [10, 30, 100, 200, 400, 800, 1600]

# Define the path to save the results
results_path = f'./experiments/global_optimum/solutions/'

for instance in instances:

    # Load the problem instance
    problem = loadInstance("data_" + str(instance), quiet=True)

    # Initialize and run the exact algorithm with no time limit
    algorithm = ExactAlgorithm(time_limit=3600*2, use_initial_solution=True)
    solution = algorithm.solve(problem)

    # Save the solution to the specified results path
    PersistSingleSolution().save(solution=solution,
                                 filename=f"globopt_{instance}",
                                 filepath=results_path)
