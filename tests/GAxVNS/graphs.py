import numpy as np
import matplotlib.pyplot as plt

# Carregar os dados dos arquivos .npz
ga_data = np.load('./tests/GAxVNS/results/solutions_1600_GA_FX.npz')
vns_data = np.load('./tests/GAxVNS/results/solutions_1600_VNS.npz')

# Extrair os arrays
ga_fx = ga_data['fx_array']
vns_fx = vns_data['fx_array']

# Criar o boxplot
plt.figure(figsize=(8, 6))
plt.boxplot([ga_fx, vns_fx], labels=['GA', 'VNS'])

# Adicionar título e rótulos
plt.title('Comparison of Objective Function Values (Instance Size = 1600)')
plt.ylabel('Objective Function Value')
plt.grid(True)

# Mostrar o gráfico
plt.tight_layout()
plt.show()
