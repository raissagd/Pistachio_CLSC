import sys
sys.path.append(r'C:\Users\Acer\Documents\IC')  
from Classes.Problem import Problem
from Classes.Algorithm import ExactAlgorithm
import numpy as np

data = Problem()
data_size = [1, 2, 3, 4, 5, 6, 7, 8]
small_solutions = []

for i in data_size:
    data.loadFile("data/small/problem_" + str(i) + ".npz")
    gurobi = ExactAlgorithm()
    solution = gurobi.solve(data)
    small_solutions.append(solution)

np.savez('small_solutions.npz', small_solutions=small_solutions)