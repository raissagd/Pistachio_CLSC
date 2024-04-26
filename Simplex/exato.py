import numpy as np
from numpy.random import uniform
import gurobipy as grb

# Tamanho único
""" SIZE = 100
I = SIZE
J = SIZE
K = SIZE
E = SIZE
Q = SIZE
S = SIZE
N1 = SIZE
N2 = SIZE
N3 = SIZE
M = SIZE """

# Test 24
I = 200
J = 62
K = 30
E = 22
Q = 130
S = 24
N1 = 400
N2 = 138
N3 = 80
M = 250

beta = 0.3
theta1 = 0.4
theta2 = 0.1
theta3 = 0.5
gammaq = 0.6
gammas = 2.
gammak = 1.01
lamb = 0.4

Fu = uniform(20000, 40000, size=J)
Fy = uniform(10000, 20000, size=Q)
Fw = uniform(20000, 50000, size=K)
Fr = uniform(4000, 8000, size=E)
Fv = uniform(40000, 80000, size=S)
CI = uniform(80, 120, size=I)
Cy = uniform(50, 100, size=Q)
Cw = uniform(100, 150, size=K)
Cr = uniform(40, 80, size=E)
Cv = uniform(150, 180, size=S)
Cu1 = uniform(60, 100, size=J)
Cu2 = uniform(80, 120, size=J)
CX = uniform(20, 40, size=(I, J))
CK = uniform(20, 40, size=(J, K))
CE = uniform(20, 40, size=(J, E))
CJ = uniform(20, 40, size=(J, Q))
CS = uniform(20, 40, size=(E, S))
CN = uniform(20, 40, size=(E, N2))
CQ = uniform(20, 40, size=(E, Q))
Cl = uniform(20, 40, size=(S, N3))
Cp = uniform(20, 40, size=(K, N1))
Cd = uniform(20, 40, size=(Q, M))

Cpa = uniform(80000, 100000, size=I)
Cpu = uniform(20000, 40000, size=J)
Cpy = uniform(20000, 40000, size=Q)
Cpw = uniform(20000, 40000, size=K)
Cpr = uniform(20000, 40000, size=E)
Cpv = uniform(20000, 40000, size=S)
Dc = uniform(200, 500, size=M)
Dp = uniform(200, 400, size=N1)
Du = uniform(100, 200, size=N2)
Ds = uniform(20, 80, size=N3)

# Criação do modelo
modelo = grb.Model(
    """Otimização de rede de cadeia de abastecimento de pistache com 
    realimentação"""
)

# Variáveis de decisão positivas: fluxos de produtos
X = modelo.addVars(int(I), int(J), vtype=grb.GRB.CONTINUOUS, name="X", lb=0.)
Go = modelo.addVars(J, K, vtype=grb.GRB.CONTINUOUS, name="Go", lb=0.)
Gr = modelo.addVars(J, E, vtype=grb.GRB.CONTINUOUS, name="Gr", lb=0.)
Gw = modelo.addVars(J, Q, vtype=grb.GRB.CONTINUOUS, name="Gw", lb=0.)
O = modelo.addVars(E, N2, vtype=grb.GRB.CONTINUOUS, name="O", lb=0.)
Oc = modelo.addVars(E, S, vtype=grb.GRB.CONTINUOUS, name="Oc", lb=0.)
Ow = modelo.addVars(E, Q, vtype=grb.GRB.CONTINUOUS, name="Ow", lb=0.)
L = modelo.addVars(S, N3, vtype=grb.GRB.CONTINUOUS, name="L", lb=0.)
P = modelo.addVars(K, N1, vtype=grb.GRB.CONTINUOUS, name="P", lb=0.)
D = modelo.addVars(Q, M, vtype=grb.GRB.CONTINUOUS, name="D", lb=0.)

# Variáveis binárias: indicadores de ativação
U = modelo.addVars(J, vtype=grb.GRB.BINARY, name="U")
Y = modelo.addVars(Q, vtype=grb.GRB.BINARY, name="Y")
W = modelo.addVars(K, vtype=grb.GRB.BINARY, name="W")
R = modelo.addVars(E, vtype=grb.GRB.BINARY, name="R")
V = modelo.addVars(S, vtype=grb.GRB.BINARY, name="V")

# Custo de abertura de instalações
z1 = (grb.quicksum(Fu[j]*U[j] for j in range(J))
      + grb.quicksum(Fy[q]*Y[q] for q in range(Q))
      + grb.quicksum(Fw[k]*W[k] for k in range(K))
      + grb.quicksum(Fr[e]*R[e] for e in range(E))
      + grb.quicksum(Fv[s]*V[s] for s in range(S)))

# Custo de produção
z2 = (grb.quicksum(CI[i]*X[i,j] for i in range(I) for j in range(J))
      + grb.quicksum(Cu1[j]*Go[j,k] for j in range(J) for k in range(K))
      + grb.quicksum(Cu2[j]*Gr[j,e] for j in range(J) for e in range(E))
      + grb.quicksum(Cy[q]*D[q,m] for q in range(Q) for m in range(M))
      + grb.quicksum(Cw[k]*P[k,n1] for k in range(K) for n1 in range(N1))
      + grb.quicksum(Cr[e]*O[e,n2] for e in range(E) for n2 in range(N2))
      + grb.quicksum(Cr[e]*Oc[e,s] for e in range(E) for s in range(S))
      + grb.quicksum(Cv[s]*L[s,n3] for s in range(S) for n3 in range(N3)))

# Custos de transporte
z3 = (grb.quicksum(CX[i,j]*X[i,j] for i in range(I) for j in range(J))
      + grb.quicksum(CK[j,k]*Go[j,k] for j in range(J) for k in range(K))
      + grb.quicksum(CE[j,e]*Gr[j,e] for j in range(J) for e in range(E))
      + grb.quicksum(CJ[j,q]*Gw[j,q] for j in range(J) for q in range(Q))
      + grb.quicksum(CS[e,s]*Oc[e,s] for e in range(E) for s in range(S))
      + grb.quicksum(CN[e,n2]*O[e,n2] for e in range(E) for n2 in range(N2))
      + grb.quicksum(CQ[e,q]*Ow[e,q] for e in range(E) for q in range(Q))
      + grb.quicksum(Cl[s, n3]*L[s,n3] for s in range(S) for n3 in range(N3))
      + grb.quicksum(Cp[k,n1]*P[k,n1] for k in range(K) for n1 in range(N1))
      + grb.quicksum(Cd[q,m]*D[q,m] for q in range(Q) for m in range(M)))

    
# Definindo a função objetivo
modelo.setObjective(z1 + z2 + z3, grb.GRB.MINIMIZE)

# Restrição de capacidade
modelo.addConstrs(
    (grb.quicksum(X[i,j] for j in range(J)) <= Cpa[i] for i in range(I)), 
    name="Eq.(4)"
)
modelo.addConstrs(
    (grb.quicksum(X[i,j] for i in range(I)) <= Cpu[j]*U[j] for j in range(J)), 
    name="Eq.(5)"
)
modelo.addConstrs(
    (grb.quicksum(Ow[e,q] for e in range(E))
     + grb.quicksum(Gw[j,q] for j in range(J)) 
     <= Cpy[q]*Y[q] for q in range(Q)), name="Eq.(6)"
)
modelo.addConstrs(
    (grb.quicksum(Go[j,k] for j in range(J)) <= Cpw[k]*W[k] for k in range(K)),
    name="Eq.(7)"
)
modelo.addConstrs(
    (grb.quicksum(Gr[j,e] for j in range(J)) <= Cpr[e]*R[e] for e in range(E)), 
    name="Eq.(8)"
)
modelo.addConstrs(
    (grb.quicksum(Oc[e,s] for e in range(E)) <= Cpv[s]*V[s] for s in range(S)),
    name="Eq.(9)"
)
modelo.addConstrs(
    (grb.quicksum(Go[j,k] for k in range(K))
     + grb.quicksum(Gr[j,e] for e in range(E))
     + grb.quicksum(Gw[j,q] for q in range(Q))
     <= grb.quicksum(X[i,j] for i in range(I)) for j in range(J)),
    name="Eq.(10)"
)
modelo.addConstrs(
    (grb.quicksum(Go[j,k] for k in range(K))
     == (1-beta)*theta1*grb.quicksum(X[i,j] for i in range(I)) for j in range(J)),
    name="Eq.(11)"
)
modelo.addConstrs(
    (grb.quicksum(Gr[j,e] for e in range(E))
     == (1-beta)*theta2*grb.quicksum(X[i,j] for i in range(I)) for j in range(J)),
    name="Eq.(12)"
)
modelo.addConstrs(
    (grb.quicksum(Gw[j,q] for q in range(Q))
     == theta3*grb.quicksum(X[i,j] for i in range(I)) for j in range(J)), 
    name="Eq.(13)"
)
modelo.addConstrs(
    (grb.quicksum(P[k,n1] for n1 in range(N1))
     <= gammak*grb.quicksum(Go[j,k] for j in range(J)) for k in range(K)),
    name="Eq.(14)"
)
modelo.addConstrs(
    (grb.quicksum(O[e,n2] for n2 in range(N2)) 
     + grb.quicksum(Oc[e,s] for s in range(S)) 
     <= (1-lamb)*grb.quicksum(Gr[j,e] for j in range(J)) for e in range(E)), 
    name="Eq.(15)"
)
modelo.addConstrs(
    (grb.quicksum(Ow[e,q] for q in range(Q))
     <= lamb*grb.quicksum(Gr[j,e] for j in range(J)) for e in range(E)), 
    name="Eq.(16)"
)
modelo.addConstrs(
    (grb.quicksum(L[s,n3] for n3 in range(N3)) 
     <= gammas*grb.quicksum(Oc[e,s] for e in range(E)) for s in range(S)),
    name="Eq.(17)"
)
modelo.addConstrs(
    (grb.quicksum(D[q,m] for m in range(M))
     <= gammaq*(grb.quicksum(Gw[j,q] for j in range(J)) 
                + grb.quicksum(Ow[e,q] for e in range(E))) for q in range(Q)), 
    name="Eq.(18)"
)
modelo.addConstrs(
    (grb.quicksum(P[k,n1] for k in range(K)) >= Dp[n1] for n1 in range(N1)), 
    name="Eq.(19)"
)
modelo.addConstrs(
    (grb.quicksum(O[e,n2] for e in range(E)) >= Du[n2] for n2 in range(N2)), 
    name="Eq.(20)"
)
modelo.addConstrs(
    (grb.quicksum(L[s,n3] for s in range(S)) >= Ds[n3] for n3 in range(N3)), 
    name="Eq.(21)"
)
modelo.addConstrs(
    (grb.quicksum(D[q,m] for q in range(Q)) <= Dc[m] for m in range(M)),
    name="Eq.(22)"
)

# Resolvendo o modelo
modelo.optimize()
variaveis_decisao = modelo.getVars()