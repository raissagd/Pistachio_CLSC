import sys
sys.path.append(r'C:\Users\Lenovo\Documents\IC')
from Classes.Problem import Problem
from Classes.Algorithm import ExactAlgorithm
import numpy as np

data = Problem()
# data_size = [100, 200, 400, 800, 1600]
solutions = []

data.loadFile("data/data_400.npz")
gurobi = ExactAlgorithm()
solution = gurobi.solve(data)
solutions.append(solution)
np.savez('tests/final_set_gurobi/solution_400.npz', solutions=solutions)