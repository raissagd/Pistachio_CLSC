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

data = Problem()
data.loadFile("data/data.npz")

best_FX_values = np.zeros((2, 30))
iter = 1

for i in range(2):
    for j in range(30):
        print(f"Execution {iter}")
        iter += 1
        vns = VariableNeighborhoodSearch([Swap(5), Reversion(4), Insertion(3), Slide(2)], 100000, i)
        solution = vns.solve(data)
        best_FX_values[i, j] = solution.FX
    
np.savez("data/best_FX_values.npz", best_FX_values=best_FX_values)