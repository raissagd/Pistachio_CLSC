import sys
sys.path.append(r'C:\Users\Lenovo\Documents\IC')
from Classes.Problem import Problem
from Classes.Algorithm import VariableNeighborhoodSearch
from Classes.Neighborhood import Swap, Reversion, Insertion, Slide, ETN, RS, SPS, SRPS
import time

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

sets = []
sets.append([Swap(2), Reversion(2), Insertion(2), Slide(2)])
sets.append([ETN(2), RS(2), SPS(2), SRPS(2)])
sets.append([Swap(2), Reversion(2), ETN(2), RS(2)])

data = Problem()
data.loadFile("data/data_800.npz")
times = []

for j in range(len(sets)):
    # Record the start time
    start_time = time.time()

    vns = VariableNeighborhoodSearch(sets[j], 100000, 1)
    solution = vns.solve(data)

    # Record the end time
    end_time = time.time()

    times.append(end_time - start_time)

print(times)
print(calculate_average(times))