from Classes.Problem import Problem
from Classes.Solution import Solution
from Classes.Algorithm import IteratedLocalSearch, VariableNeighborhoodSearch
from Classes.Neighborhood import Swap, Reversion, Insertion, Slide, ETN, RS, SPS, SRPS, MinMaxSwap, SourceDepotSwap, ENS
import random
import numpy as np

"""
1) Gerar um problema padrão e salvar
2) Definir um conjunto de formulações do VNS
3) Rodar 30 vezes cada algoritmo e guardar o melhor f(x) de cada execução
   - Todo mundo com o mesmo critério de parada: 100 mil avaliações
"""

I, J, K, E, Q, S, N1, N2, N3, M = 10, 10, 10, 10, 10, 10, 10, 10, 10, 10

def createProblem(I, J, K, E, Q, S, N1, N2, N3, M):
    problem = Problem()
    problem.generate(I, J, K, E, Q, S, N1, N2, N3, M)
    problem.saveFile("data/data.npz")
    
def find_smallest_FX(arr):
    smallest = arr[0]  # Assume the first element is the smallest
    for num in arr:
        if num < smallest:
            smallest = num  # Update smallest if a smaller value is found
    return smallest

def VNSSets(data):
    sets = []
    sets.append([Swap(5), Reversion(4), Insertion(3), Slide(2)])
    sets.append([ETN(6), RS(6), SPS(5), SRPS(2)])
    sets.append([MinMaxSwap(5), SourceDepotSwap(2, data), ENS(1)])
    return sets

data = Problem()
data.loadFile("data/data.npz")

sets = VNSSets(data)
best_FX_values = np.zeros((len(sets), 30))

for i in range(len(sets)):
    for j in range(2):
        vns = VariableNeighborhoodSearch(sets[i], 100000)
        solution = vns.solve(data)
        best_FX_values[i, j] = solution.FX
    
np.savez("data/best_FX_values.npz", best_FX_values=best_FX_values)