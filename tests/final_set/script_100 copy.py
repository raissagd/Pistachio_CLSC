import sys
sys.path.insert(0, 'Classes/')
from Problem import Problem
from Algorithm import VariableNeighborhoodSearch
from Neighborhood import Swap, Reversion, Insertion, Slide, ETN, RS, SPS, SRPS
from Execute import RunMultipleMethodsMultipleTimes
from Persistence import PersistMultipleSolutions
import numpy as np


number_evaluations = 300
vns1 = VariableNeighborhoodSearch([Swap(2), Reversion(2), Insertion(2), Slide(2)], number_evaluations, 1)
vns2 = VariableNeighborhoodSearch([ETN(2), RS(2), SPS(2), SRPS(2)], number_evaluations, 1)
vns3 = VariableNeighborhoodSearch([Swap(2), Reversion(2), ETN(2), RS(2)], number_evaluations, 1)
methods = [vns1, vns2, vns3]
number_executions = 30

data = Problem()
data.loadFile("data/data_100.npz")

results = RunMultipleMethodsMultipleTimes().run(data, methods, number_executions)

PersistMultipleSolutions().save(results, 'scrip_100_final_set', './tests/final_set/results/')


# solutions = np.zeros((len(sets), 30))
# iter = 1

# # 1 = stochastic
# for j in range(len(sets)):
#         for k in range(30):
#             print(f"Execution {iter}")
#             iter += 1
#             vns = VariableNeighborhoodSearch(sets[j], 100000, 1)
#             solution = vns.solve(data)
#             solutions[j, k] = solution.FX
# np.savez(f"solutions_100.npz", solutions=solutions)