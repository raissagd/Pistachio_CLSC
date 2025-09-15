import sys
sys.path.insert(0, 'Classes/')
from Problem import Problem
from Persistence import PersistSingleSolution
from Algorithm import ExactAlgorithm

instance = '10'

problem_file = f'data_{instance}.npz'
problem_path = f'./data'
result_path = f'./tests/exact_novo/results'

problem = Problem()
problem.loadFile(f'{problem_path}/{problem_file}')

exact = ExactAlgorithm(time_limit=None)  # Sem limite de tempo
solution = exact.solve(problem)

PersistSingleSolution().save(solution=solution, filename=f'inst_{instance}',filepath=result_path)

