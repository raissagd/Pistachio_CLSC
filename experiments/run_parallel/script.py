import sys
sys.path.insert(0, 'Classes/')
from Problem import Problem
from Algorithm import VariableNeighborhoodSearch
from Neighborhood import Swap, Reversion, Insertion, Slide, ETN, RS, SPS, SRPS, FixedCostSwap, TransportCostSwap, SourceCostBoost
from Execute import RunMultipleMethodsMultipleTimes
from Persistence import PersistMultipleSolutions
import pandas as pd

number_evaluations = 1000
""" vns1 = VariableNeighborhoodSearch([Swap(2), Reversion(2), Insertion(2), Slide(2)], number_evaluations, 1, name='VNS_Swap')
vns2 = VariableNeighborhoodSearch([ETN(2), RS(2), SPS(2), SRPS(2)], number_evaluations, 1, name='VNS_ETN')
vns3 = VariableNeighborhoodSearch([Swap(2), Reversion(2), ETN(2), RS(2)], number_evaluations, 1, name='VNS_SwapETN') """
# vns4 = VariableNeighborhoodSearch([Reversion(2), Reversion(2), Reversion(2), Reversion(2)], number_evaluations, 1, name='VNS_Reversion')

data = Problem()
data.loadFile("data/data_30.npz")

#vns1 = VariableNeighborhoodSearch([FixedCostSwap(3, data)], number_evaluations, 1, name='teste')
#vns1 = VariableNeighborhoodSearch([Reversion(2)], number_evaluations, 1, name='teste')
vns1 = VariableNeighborhoodSearch([Reversion(2), SourceCostBoost(2, data)], number_evaluations, 1, name='teste')
#vns1 = VariableNeighborhoodSearch([TransportCostSwap(2, data)], number_evaluations, 1, name='teste')
#vns1 = VariableNeighborhoodSearch([SourceCostBoost(2, data)], number_evaluations, 1, name='teste')
methods = [vns1]
number_executions = 30

results = RunMultipleMethodsMultipleTimes().run(data, methods, number_executions, log=False)

# PersistMultipleSolutions().save(results, 'teste', './', log=False)

fx_values = [sol.FX for sol in results[0][0]]

df_fx = pd.DataFrame({"Execution": list(range(1, len(fx_values) + 1)),"FX": fx_values})
df_fx.to_csv("teste.csv", index=False, sep=";")

df_lido = pd.read_csv("teste.csv", sep=";")
media_fx = df_lido["FX"].mean()
media_formatada = f"{media_fx:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
print(f"Média FX: {media_formatada}")