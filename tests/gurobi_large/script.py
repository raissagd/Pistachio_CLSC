import sys
sys.path.append(r'C:\Users\Acer\Documents\IC')  
from Classes.Problem import Problem
from Classes.Algorithm import ExactAlgorithm
import numpy as np

data = Problem()
data_size = [17, 18, 19, 20, 21, 22, 23, 24]
large_solutions = []

for i in data_size:
    data.loadFile("data/large/problem_" + str(i) + ".npz")
    gurobi = ExactAlgorithm()
    solution = gurobi.solve(data)
    large_solutions.append(solution)

np.savez('large_solutions.npz', large_solutions=large_solutions)