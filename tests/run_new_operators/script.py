import sys
sys.path.insert(0, 'Classes/')
from Problem import Problem
from Algorithm import VariableNeighborhoodSearch
from Neighborhood import Reversion, RS, TransportCostSwap, SourceCostBoost
from Execute import RunMultipleMethodsMultipleTimes
from Persistence import PersistMultipleSolutions
import pandas as pd

number_evaluations = 1000

data = Problem()
data.loadFile("data/data_100.npz")

vns1 = VariableNeighborhoodSearch([Reversion(2), RS(2), TransportCostSwap(2, data), SourceCostBoost(2, data)], number_evaluations, 1, name='teste')
methods = [vns1]
number_executions = 30

results = RunMultipleMethodsMultipleTimes().run(data, methods, number_executions, log=False)

PersistMultipleSolutions().save(results, 'teste', './', log=False)

""" fx_values = [sol.FX for sol in results[0][0]]

df_fx = pd.DataFrame({"Execution": list(range(1, len(fx_values) + 1)),"FX": fx_values})
df_fx.to_csv("teste.csv", index=False, sep=";")

df_lido = pd.read_csv("teste.csv", sep=";")
media_fx = df_lido["FX"].mean()
media_formatada = f"{media_fx:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
print(f"Média FX: {media_formatada}") """