import sys
sys.path.append(r'C:\Users\Lenovo\Documents\IC')
from Classes.Problem import Problem
from Classes.Algorithm import IteratedLocalSearch, VariableNeighborhoodSearch
from Classes.Neighborhood import Swap, Reversion, Insertion, Slide, ETN, RS, SPS, SRPS
import numpy as np

sets = []
sets.append([Swap(2), Reversion(2), Insertion(2), Slide(2)])
sets.append([ETN(2), RS(2), SPS(2), SRPS(2)])
sets.append([Swap(2), Reversion(2), ETN(2), RS(2)])

data = Problem()
data.loadFile("data/data_30.npz")

solutions = np.zeros((len(sets), 30))
iter = 1

for j in range(len(sets)):
        for k in range(30):
            print(f"Execution {iter}")
            iter += 1
            vns = IteratedLocalSearch(sets[j], 100)
            solution = vns.solve(data)
            solutions[j, k] = solution.FX
np.savez(f"solutions_30_ILS.npz", solutions=solutions)