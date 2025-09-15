import sys
sys.path.append(r'../../')
from Classes.Persistence import PersistMultipleSolutions
import numpy as np

# Load the solutions from the pickle file
persist = PersistMultipleSolutions()
solutions = persist.load(filename='script_100', filepath='./new_results/')

# Extract the FX attribute
try:
    fx_values = [solution.execution_time for outer_list in solutions for middle_list in outer_list for solution in middle_list]
except AttributeError as e:
    print(f"Error: {e}")

# Convert the list to a numpy array if fx_values is defined
if 'fx_values' in locals():
    fx_array = np.array(fx_values)
    # Save the array to a .npz fileS
    np.savez('./new_results/script_100_execution_time.npz', fx_array=fx_array)