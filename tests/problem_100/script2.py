import sys
sys.path.append(r'C:\Users\Acer\Documents\IC') 
from Classes.Problem import Problem
from Classes.Algorithm import VariableNeighborhoodSearch
from Classes.Neighborhood import Swap, Reversion, Insertion, Slide, ETN, RS, SPS, SRPS, MinMaxSwap, SourceDepotSwap, ENS
import numpy as np

I, J, K, E, Q, S, N1, N2, N3, M = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100

def createProblem(I, J, K, E, Q, S, N1, N2, N3, M):
    problem = Problem()
    problem.generate(I, J, K, E, Q, S, N1, N2, N3, M)
    problem.saveFile("data/data_100.npz")

def VNSSets(data):
    sets = []
    sets.append([Swap(1), Reversion(1), Insertion(1), Slide(1)])
    sets.append([Swap(2), Reversion(2), Insertion(2), Slide(2)])
    sets.append([Swap(3), Reversion(3), Insertion(3), Slide(3)])
    sets.append([Swap(4), Reversion(4), Insertion(4), Slide(4)])
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
    np.savez(f"FX_values_2_{i}.npz", FX_values_=FX_values)