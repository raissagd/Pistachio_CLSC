import sys
sys.path.insert(0, 'Classes/')
from Problem import loadInstance
from Persistence import PersistSingleSolution
from Algorithm import ExactAlgorithm

instances = [10, 30, 100, 200, 400, 800, 1600]
results_path = f'./experiments/global_optimum/solutions/'

for instance in instances:
    problem = loadInstance("data_" + str(instance), quiet=True)
    algorithm = ExactAlgorithm(time_limit=None)
    solution = algorithm.solve(problem)
    PersistSingleSolution().save(solution=solution,
                                 filename=f"globopt_{instance}",
                                 filepath=results_path)
