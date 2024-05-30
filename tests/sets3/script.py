import sys
sys.path.append(r'C:\Users\Acer\Documents\IC')  
from Classes.Problem import Problem
from Classes.Algorithm import VariableNeighborhoodSearch
from Classes.Neighborhood import Swap, Reversion, Insertion, Slide, ETN, RS, SPS, SRPS, MinMaxSwap, SourceDepotSwap, ENS
import numpy as np

def VNSSets(data):
    sets = []
    sets.append([Swap(5), Swap(4), Swap(3), Swap(2), Swap(1)])
    sets.append([Swap(1), Swap(2), Swap(3), Swap(4), Swap(5)])
    return sets

data = Problem()
data.loadFile("data/data_100.npz")

sets = VNSSets(data)
FX_values = np.zeros((len(sets), 30))
iter = 1

# i = 0 -> Deterministic
# i = 1 -> Stochastic
for i in range(2):
    print(f"Starting execution {i}")
    for j in range(len(sets)):
        for k in range(30):
            print(f"Execution {iter}")
            iter += 1
            vns = VariableNeighborhoodSearch(sets[j], 100000, i)
            solution = vns.solve(data)
            FX_values[j, k] = solution.FX
    np.savez(f"FX_values_3_{i}.npz", FX_values_=FX_values)