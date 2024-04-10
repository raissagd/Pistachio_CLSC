from Problem import Problem
from Solution import Solution
from Algorithm import IteratedLocalSearch, VariableNeighborhoodSearch
from Neighborhood import Swap, Reversion, Insertion, MaxMinSwap, Slide, ETN, RS, SPS, SRPS

I, J, K, E, Q, S, N1, N2, N3, M = 3, 2, 1, 1, 1, 1, 2, 2, 1, 2
# I, J, K, E, Q, S, N1, N2, N3, M = 9, 6, 3, 2, 5, 3, 8, 4, 4, 8

# Creating an instance of the Problem class
""" problem = Problem()
problem.generate(I, J, K, E, Q, S, N1, N2, N3, M)
problem.saveFile("data.npz") """
data = Problem()
data.loadFile("data.npz")

# Creating an instance of the Solution class
""" solution = Solution()
solution.generateChromosome(data)
solution.evaluate(data)
solution.check(data)   """

#ILS = IteratedLocalSearch([Swap(2), Reversion(2), Insertion(2), MaxMinSwap(2), Slide(2), ETN(2), RS(2), SPS(2), SRPS(2)], 5)
#ILS.solve(data)
VNS = VariableNeighborhoodSearch([Swap(5), Reversion(10), Insertion(4), MaxMinSwap(5), Slide(6), ETN(5), RS(5), SPS(3), SRPS(4)], 50)
VNS.solve(data)

# mudança no s8
# errros n tem compostagem suficiente
# por que implementar os dois?