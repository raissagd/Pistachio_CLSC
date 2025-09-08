import sys
sys.path.insert(0, 'Classes/')
from Problem import Problem
from Algorithm import VariableNeighborhoodSearch, VariableNeighborhoodSearch2
from Neighborhood import Reversion, Slide, Insertion, Swap
from Execute import RunMultipleMethodsMultipleTimes
from Persistence import PersistMultipleSolutions
import pandas as pd

number_evaluations = 25000

data = Problem()
data.loadFile("data/data_400.npz")

vns1 = VariableNeighborhoodSearch2([Swap(2), Reversion(2), Insertion(2), Slide(2)], number_evaluations, 1, name='VNS_Swap')
methods = [vns1]
number_executions = 30

results = RunMultipleMethodsMultipleTimes().run(data, methods, number_executions, log=False)

#PersistMultipleSolutions().save(results, 'teste', './', log=False)

fx_values = [sol.FX for sol in results[0][0]]
eval_values = [sol.n_eval for sol in results[0][0]]

df_fx = pd.DataFrame({
    "Execution": list(range(1, len(fx_values) + 1)),
    "FX": fx_values,
    "Evaluations": eval_values
})

df_fx.to_csv("./tests/new_VNS/instance_400/VNS2.csv", index=False, sep=";")