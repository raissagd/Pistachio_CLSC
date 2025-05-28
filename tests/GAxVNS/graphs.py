import numpy as np
import matplotlib.pyplot as plt

# Carregar os dados dos arquivos .npz
ga_data = np.load('./tests/GAxVNS/new_results/GA_400_FX.npz')['fx_array']
vns_data = np.load('./tests/run_parallel/new_results/script_400_fx_values.npz')['fx_array']

# Extrair os arrays
vns_fx = vns_data[:30]

# Criar o boxplot
plt.figure(figsize=(8, 6))
plt.boxplot([ga_data, vns_fx], labels=['GA', 'VNS'], notch=True)

# Adicionar título e rótulos
plt.title('Comparison of Objective Function Values (Instance Size = 400)')
plt.ylabel('Objective Function Value')
plt.grid(True)

# Mostrar o gráfico
plt.tight_layout()
plt.show()
