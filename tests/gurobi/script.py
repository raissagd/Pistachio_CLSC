import sys
sys.path.insert(0, 'Classes/')
from Problem import Problem
from Algorithm import ExactAlgorithm
import numpy as np

data = Problem()
data_size = [10, 30, 100]
all_solutions = []

for i in data_size:
    data.loadFile("data/data_" + str(i) + ".npz")
    gurobi = ExactAlgorithm()
    solution = gurobi.solve(data)
    all_solutions.append(solution)

np.savez('all_solutions.npz', all_solutions=all_solutions)