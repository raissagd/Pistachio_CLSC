import sys
sys.path.append(r'C:\Users\Acer\Documents\IC')  
from Classes.Problem import Problem
from Classes.Algorithm import ExactAlgorithm
import numpy as np

data = Problem()
data_size = [9, 10, 11, 12, 13, 14, 15, 16]
medium_solutions = []

for i in data_size:
    data.loadFile("data/medium/problem_" + str(i) + ".npz")
    gurobi = ExactAlgorithm()
    solution = gurobi.solve(data)
    medium_solutions.append(solution)

np.savez('medium_solutions.npz', medium_solutions=medium_solutions)