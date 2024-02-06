import numpy as np

data = np.load("data.npz")

# Lista de variáveis a serem extraídas
variaveis = ["I", "K", "J", "E", "Q", "S", "N1", "N2", "N3", "M", 
             "Fu", "Fy", "Fw", "Fr", "Fv", "CI", "Cy", "Cw", "Cr", 
             "Cv", "Cu1", "Cu2", "CX", "CK", "CE", "CJ", "CS", "CN", 
             "CQ", "Cl", "Cp", "Cd", "Beta", "Theta", "yq", "ys", "yk", 
             "lambd", "Cpa", "Cpu", "Cpy", "Cpw", "Cpr", "Cpv", "Dc", 
             "Dp", "Du", "Ds"]

# Atribuir os valores correspondentes às variáveis
for variavel in variaveis:
    globals()[variavel] = data[variavel]

data.close()