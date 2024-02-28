import numpy as np

I, J, K, E, Q, S, N1, N2, N3, M = [3, 2, 1, 1, 1, 1, 2, 2, 1, 2]

# Fixed costs
Fu = np.random.uniform(low=20000, high=40000, size=J)
Fy = np.random.uniform(low=10000, high=20000, size=Q)
Fw = np.random.uniform(low=20000, high=50000, size=K)
Fr = np.random.uniform(low=4000, high=8000, size=E)
Fv = np.random.uniform(low=40000, high=80000, size=S)

# Production costs
CI = np.random.uniform(low=80, high=120, size=I)
Cy = np.random.uniform(low=50, high=100, size=Q)
Cw = np.random.uniform(low=100, high=150, size=K)
Cr = np.random.uniform(low=40, high=80, size=E)
Cv = np.random.uniform(low=150, high=180, size=S)
Cu1 = np.random.uniform(low=60, high=100, size=J)
Cu2 = np.random.uniform(low=80, high=120, size=J)

# Shipping costs
CX = np.random.uniform(low=20, high=40, size=(I, J))
CK = np.random.uniform(low=20, high=40, size=(J, K))
CE = np.random.uniform(low=20, high=40, size=(J, E))
CJ = np.random.uniform(low=20, high=40, size=(J, Q))
CS = np.random.uniform(low=20, high=40, size=(E, S))
CN = np.random.uniform(low=20, high=40, size=(E, N2))
CQ = np.random.uniform(low=20, high=40, size=(E, Q))
Cl = np.random.uniform(low=20, high=40, size=(S, N3))
Cp = np.random.uniform(low=20, high=40, size=(K, N1))
Cd = np.random.uniform(low=20, high=40, size=(Q, M))

# Parameters
beta = 0.3
theta = [0.4, 0.1, 0.5]
gammaq = 0.6
gammas = 2
gammak = 1.01
lamb = 0.4

# Production capacities and demands
Cpa = np.random.uniform(low=80000, high=100000, size=I)
Cpu = np.random.uniform(low=20000, high=40000, size=J)
Cpy = np.random.uniform(low=20000, high=40000, size=Q)
Cpw = np.random.uniform(low=20000, high=40000, size=K)
Cpr = np.random.uniform(low=20000, high=40000, size=E)
Cpv = np.random.uniform(low=20000, high=40000, size=S)
Dc = np.random.uniform(low=200, high=400, size=M)
Dp = np.random.uniform(low=200, high=400, size=N1)
Du = np.random.uniform(low=100, high=200, size=N2)
Ds = np.random.uniform(low=20, high=80, size=N3)

np.savez_compressed("data.npz", I=I, K=K, J=J, E=E, Q=Q, S=S, N1=N1, N2=N2, N3=N3, M=M, Fu=Fu, Fy=Fy, Fw=Fw, Fr=Fr, Fv=Fv, CI=CI, Cy=Cy, Cw=Cw, Cr=Cr, Cv=Cv, Cu1=Cu1, Cu2=Cu2, CX=CX, CK=CK, CE=CE, CJ=CJ, CS=CS, CN=CN, CQ=CQ, Cl=Cl, Cp=Cp, Cd=Cd, beta=beta, theta=theta, gammaq=gammaq, gammas=gammas, gammak=gammak, lamb=lamb, Cpa=Cpa, Cpu=Cpu, Cpy=Cpy, Cpw=Cpw, Cpr=Cpr, Cpv=Cpv, Dc=Dc, Dp=Dp, Du=Du, Ds=Ds)