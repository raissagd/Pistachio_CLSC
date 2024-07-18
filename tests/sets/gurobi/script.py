import sys
sys.path.insert(0, 'Classes/')
from Problem import Problem
from Algorithm import ExactAlgorithm
import numpy as np

data = Problem()
data_size = [200, 400, 800]
all_solutions = []

for i in data_size:
    data.loadFile("data/data_" + str(i) + ".npz")
    gurobi = ExactAlgorithm()
    solution = gurobi.solve(data)
    all_solutions.append(solution)

np.savez('all_solutions_v2.npz', all_solutions=all_solutions)