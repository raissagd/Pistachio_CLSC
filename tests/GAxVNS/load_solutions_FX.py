import sys
sys.path.append(r'../../')
from Classes.Persistence import PersistMultipleSolutions
import numpy as np

# Carregar as soluções do arquivo pickle
persist = PersistMultipleSolutions()
solutions = persist.load(filename='GA_800', filepath='./new_results/')

# Extrair o atributo FX de cada solução
try:
    fx_values = [solution.FX for outer_list in solutions for middle_list in outer_list for solution in middle_list]
except AttributeError as e:
    print(f"Erro: {e}")

# Converter a lista em um array numpy, se fx_values estiver definido
if 'fx_values' in locals():
    fx_array = np.array(fx_values)
    # Salvar o array em um arquivo .npz
    np.savez('./new_results/GA_800_FX.npz', fx_array=fx_array)
