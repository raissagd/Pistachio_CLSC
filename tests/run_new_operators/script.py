import sys
sys.path.insert(0, 'Classes/')
from Problem import Problem
from Algorithm import VariableNeighborhoodSearch
from Neighborhood import Reversion, Swap, TransportCostSwap, SourceCostBoost, Slide, ETN, RS, SPS, SRPS, Insertion
from Execute import RunMultipleMethodsMultipleTimes
from Persistence import PersistMultipleSolutions

number_evaluations = 10

data = Problem()
data.loadFile("data/data_10.npz")

vns1 = VariableNeighborhoodSearch([Swap(2), Reversion(2), Insertion(2), Slide(2)], number_evaluations, 1, name='VNS_Swap')
vns2 = VariableNeighborhoodSearch([ETN(2), RS(2), SPS(2), SRPS(2)], number_evaluations, 1, name='VNS_ETN')
vns3 = VariableNeighborhoodSearch([Swap(2), Reversion(2), TransportCostSwap(2, data), SourceCostBoost(2, data)], number_evaluations, 1, name='teste')
methods = [vns1, vns2, vns3]
number_executions = 1

results = RunMultipleMethodsMultipleTimes().run(data, methods, number_executions)

PersistMultipleSolutions().save(results, 'test', './tests/run_new_operators/script_400/', log=True)