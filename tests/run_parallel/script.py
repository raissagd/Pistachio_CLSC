import sys
sys.path.insert(0, 'Classes/')
from Problem import Problem
from Algorithm import VariableNeighborhoodSearch
from Neighborhood import Swap, Reversion, Insertion, Slide, ETN, RS, SPS, SRPS
from Execute import RunMultipleMethodsMultipleTimes
from Persistence import PersistMultipleSolutions

number_evaluations = 100000
vns1 = VariableNeighborhoodSearch([Swap(2), Reversion(2), Insertion(2), Slide(2)], number_evaluations, 1)
vns2 = VariableNeighborhoodSearch([ETN(2), RS(2), SPS(2), SRPS(2)], number_evaluations, 1)
vns3 = VariableNeighborhoodSearch([Swap(2), Reversion(2), ETN(2), RS(2)], number_evaluations, 1)
methods = [vns1, vns2, vns3]
number_executions = 30

data = Problem()
data.loadFile("data/data_30.npz")

results = RunMultipleMethodsMultipleTimes().run(data, methods, number_executions)

PersistMultipleSolutions().save(results, 'script_30_results', './tests/run_parallel/results/')