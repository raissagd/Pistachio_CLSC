from Problem import Problem
from Algorithm import VariableNeighborhoodSearch
from Neighborhood import Swap, Reversion, Insertion, Slide, ETN, RS, SPS, SRPS, FixedCostSwap, TransportCostSwap
from Solution import Solution
import pickle

number_evaluations = 1000
data = Problem()
data.loadFile("data/data_10.npz")

#vns1 = VariableNeighborhoodSearch([FixedCostSwap(3, data)], number_evaluations, 1, name='teste')
#vns1 = VariableNeighborhoodSearch([Reversion(2)], number_evaluations, 1, name='teste')
vns1 = VariableNeighborhoodSearch([TransportCostSwap(2, data)], number_evaluations, 1, name='teste')

solution = Solution()
solution.generateChromosomeStochastic(data)

with open('solution_test.pickle', 'wb') as f:
    pickle.dump(solution, f)