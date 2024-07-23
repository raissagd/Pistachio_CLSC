import sys
sys.path.insert(0, 'Classes/')
from Persistence import PersistMultipleSolutions
import numpy as np

"""
Structure of this Pickle file:
1. A list of length 3 (outer list).
2. Each element in the outer list is a list of length 3 (middle list).
3. Each element in the middle list is a list of length 30 (inner list).
4. Each element in the inner list is a Solution object with an FX attribute.
"""

# Load the solutions from the pickle file
persist = PersistMultipleSolutions()
solutions = persist.load(filename='script_100_results', filepath='./tests/run_parallel/results/')

# Extract the FX attribute
try:
    fx_values = [solution.FX for outer_list in solutions for middle_list in outer_list for solution in middle_list]
except AttributeError as e:
    print(f"Error: {e}")

# Convert the list to a numpy array if fx_values is defined
if 'fx_values' in locals():
    fx_array = np.array(fx_values)
    # Save the array to a .npz fileS
    np.savez('./tests/run_parallel/results/script_100_fx_values.npz', fx_array=fx_array)