"""
This script calculates the total number of variables in a mathematical model and a priority-based representation.
Variables:
    Z (int): Base number for initializing the amount for each entity.
    I, J, K, E, Q, S, N1, N2, N3, M (int): Amount for each entity, initialized to Z.
Mathematical Model Variables:
    X (int): Number of elements for variable X, calculated as I * J.
    Go (int): Number of elements for variable Go, calculated as J * K.
    Gr (int): Number of elements for variable Gr, calculated as J * E.
    Gw (int): Number of elements for variable Gw, calculated as J * Q.
    O (int): Number of elements for variable O, calculated as E * N2.
    Oc (int): Number of elements for variable Oc, calculated as E * S.
    Ow (int): Number of elements for variable Ow, calculated as E * Q.
    L (int): Number of elements for variable L, calculated as S * N3.
    P (int): Number of elements for variable P, calculated as K * N1.
    D (int): Number of elements for variable D, calculated as Q * M.
    U, Y, W, R, V (int): Number of elements for variables U, Y, W, R, V, initialized to J, Q, K, E, S respectively.
Total Variables:
    total (int): Total number of variables in the mathematical model, calculated as the sum of all individual variables.
Priority-based Representation:
    total (int): Total number of variables in the priority-based representation, calculated as the sum of specific combinations of entities.
Output:
    Prints the total number of variables in the mathematical model and the priority-based representation.
"""

# Base number
Z = 1600

# Amount for each entity
I, J, K, E, Q, S, N1, N2, N3, M = Z, Z, Z, Z, Z, Z, Z, Z, Z, Z

# Number of elements for each variable in the mathematical model
X = I*J
Go = J*K
Gr = J*E
Gw = J*Q
O = E*N2
Oc = E*S
Ow = E*Q
L = S*N3
P = K*N1
D = Q*M
U = J
Y = Q
W = K
R = E
V = S

# Total number of variables of the mathematical model
total = X + Go + Gr + Gw + O + Oc + Ow + L + P + D + U + Y + W + R + V
print(f"Mathematical model: {total} variables")

# Total number of variables of the priority-based representation
total = I+J + J+K + K+N1 + J+E + N2+S + S+N3 + J+E+Q + Q+M
print(f"Priority-based representation: {total} variables")