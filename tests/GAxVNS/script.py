import sys
sys.path.insert(0, 'Classes/')
from Problem import Problem
from Algorithm import GeneticAlgorithm
from Execute import RunMultipleMethodsMultipleTimes
from Persistence import PersistMultipleSolutions

data = Problem()
data.loadFile("data/data_800.npz")

# Genetic Algorithm parameters
population_size = 100
crossover_rate = 0.8
mutation_rate = 0.2
max_eval = 100000
initialization = 1

# Criando a instância do algoritmo genético
ga = GeneticAlgorithm(
    population_size=population_size,
    crossover_rate=crossover_rate,
    mutation_rate=mutation_rate,
    initialization=initialization,
    max_eval=max_eval
)

# Executando o algoritmo 30 vezes em paralelo
methods = [ga]
number_executions = 30

results = RunMultipleMethodsMultipleTimes().run(data, methods, number_executions)

# Salvando as soluções em um arquivo pickle
PersistMultipleSolutions().save(results, 'solutions_800_GA', './tests/GAxVNS/results/')