from Classes.Problem import Problem
from Classes.Solution import Solution
from Classes.Algorithm import IteratedLocalSearch, VariableNeighborhoodSearch
from Classes.Neighborhood import Swap, Reversion, Insertion, Slide, ETN, RS, SPS, SRPS, MinMaxSwap, SourceDepotSwap, ENS
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

def VNSSets(data):
    sets = []
    sets.append([Swap(5), Reversion(4), Insertion(3), Slide(2)])
    sets.append([ETN(6), RS(6), SPS(5), SRPS(2)])
    sets.append([MinMaxSwap(5), SourceDepotSwap(2, data), ENS(1)])
    return sets

data = Problem()
data.loadFile("data/data.npz")

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
    np.savez(f"data/FX_values_{i}.npz", FX_values_=FX_values)