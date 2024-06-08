import sys
sys.path.append(r'C:\Users\Lenovo\Documents\IC')
from Classes.Problem import Problem
from Classes.Algorithm import VariableNeighborhoodSearch
from Classes.Neighborhood import Swap, Reversion, Insertion, Slide, ETN, RS, SPS, SRPS
import numpy as np
import os

def add_solution_to_npz(file_path, new_solution):
    # Check if the file exists
    if os.path.exists(file_path):
        # Load existing data
        data = np.load(file_path)
        solutions = data['solutions'].tolist()
    else:
        # Initialize an empty list if the file does not exist
        solutions = []

    # Append the new solution
    solutions.append(new_solution)

    # Save the updated solutions back to the .npz file
    np.savez(file_path, solutions=np.array(solutions))

sets = []
sets.append([Swap(2), Reversion(2), Insertion(2), Slide(2)])
""" sets.append([ETN(2), RS(2), SPS(2), SRPS(2)])
sets.append([Swap(2), Reversion(2), ETN(2), RS(2)]) """

data = Problem()
data.loadFile("../../data/data_800.npz")

vns = VariableNeighborhoodSearch(sets[0], 800000, 1)
solution = vns.solve(data)
new_solution = solution.FX

file_path = '/solutions_800.npz'
add_solution_to_npz(file_path, new_solution)