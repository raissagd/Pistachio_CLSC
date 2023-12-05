import decode
import read

# fluxo fábricas de pistache -> clientes de pistache

chromo = [2,5,3,6,4,1]
K = [0, 1, 2] # set of sources
J = [0, 1, 2] # set of depots
a = read.Cpw # capacity of source k
b = read.Dp # demand on depot kj
c = read.Cp # tranportation cost

print("------------------ Initial values ----------------")
print("Chromosome:", chromo)
print("Sources' capacities:", a)
print("Depots' demands:", b)
print("Transportation matrix: ", c)
print("---------------------------------------------------")
print(" ")

decode.main(K, J, b, a, c, chromo)