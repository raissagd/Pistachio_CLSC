import sys
sys.path.append(r'C:\Users\Acer\Documents\IC')
from Classes.Problem import Problem
from Classes.Algorithm import VariableNeighborhoodSearch
from Classes.Neighborhood import Swap, Reversion, Insertion, Slide
import numpy as np

def VNSSets():
    sets = []
    sets.append([Swap(4), Reversion(4), Insertion(4), Slide(4)])
    return sets

data = Problem()
sets = VNSSets()
FX_values = np.zeros((len(sets), 30))
iter = 1
data_size = [1, 2, 3, 4, 5, 6, 7, 8]

for i in data_size:
    data.loadFile("data/small/problem_" + str(i) + ".npz")
    print(f"Starting execution {i}")
    for j in range(len(sets)):
        for k in range(30):
            print(f"Execution {iter}")
            iter += 1
            vns = VariableNeighborhoodSearch(sets[j], 100000, 1)
            solution = vns.solve(data)
            FX_values[j, k] = solution.FX
    np.savez(f"set_2_problem_{i}.npz", FX_values_=FX_values)