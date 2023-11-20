import numpy

I = 3  # The producer locations (pistachlo orchard)
K = 3  # The potential processing center
J = 3  # The potential pistachio factory locations
E = 2  # The potential oil extraction center locations
Q = 2  # The potential composting center locations
S = 2  # The potential cosmetic factories locations
N1 = 3 # The pistachio market locatlons
N2 = 3 # The oil market locations
N3 = 2 # The cosmetic customer locations
M = 2  # Total compost's customers

Fu = numpy.random.uniform(low=20000, high=40000, size=J)  # Fixed cost of processing center j
Fy = numpy.random.uniform(low=10000, high=20000, size=Q)  # Fixed cost of composting center q
Fw = numpy.random.uniform(low=20000, high=50000, size=K)  # Fixed cost of pistachio factory k
Fr = numpy.random.uniform(low=4000, high=8000, size=E)    # Fixed cost of oil extraction center e
Fv = numpy.random.uniform(low=40000, high=80000, size=S)  # Fixed cost of cosmetic factory

CI = numpy.random.uniform(low=80, high=120, size=I)  # Production cost per unit of product from producer i
Cy = numpy.random.uniform(low=50, high=100, size=Q)  # Production cost per unit of product for composting center q
Cw = numpy.random.uniform(low=100, high=150, size=K) # Roasting and packing cost per unit of product for pistachio factory k
Cr = numpy.random.uniform(low=40, high=80, size=E)   # Extracting cost per unit of product for oil extraction center e
Cv = numpy.random.uniform(low=150, high=180, size=S) # Production cost per unit of products for cosmetic factory s
Cu1 = numpy.random.uniform(low=60, high=100, size=J) # Processing cost per unit of product type 1 for processing centers i
Cu2 = numpy.random.uniform(low=80, high=120, size=J) # Processing cost per unit of product type 2 for processing centers i

CX  = numpy.random.uniform(low = 20, high = 40, size = I * J) # Shipping cost per unit of picked pistachio shipped from the producer (pistachio orchard) i to processing center j
CK = numpy.random.uniform(low = 20, high = 40, size = J * K) #  Shipping cost per unit of open-mouth pistachio shipped from processing center j to pistachio factory k
CE = numpy.random.uniform(low = 20, high = 40, size = J * E) # Shipping cost per unit of raw kernel shipped from processing center j to oil extraction center e
CJ = numpy.random.uniform(low = 20, high = 40, size = J * Q) # Shipping cost per unit of processing waste shipped from processing center j to composting center q
CS = numpy.random.uniform(low = 20, high = 40, size = E * S) # Shipping cost per unit of products from oil extraction center e to cosmetic factory s
CN = numpy.random.uniform(low = 20, high = 40, size = E * N2) # Shipping cost per unit of product shipped from oil extraction center e to oil customer N2
CQ = numpy.random.uniform(low = 20, high = 40,size = E * Q) # Shipping cost per unit of products from oil extraction center e to composting center q
Cl = numpy.random.uniform(low = 20, high = 40, size = S * N3) # Shipping cost per unit of product shipped from cosmetic factory s to cosmetic customer N3
Cp = numpy.random.uniform(low = 20, high = 40, size = K * N1) # Shipping cost per unit of product shipped from pistachio factory k to pistachio customer N1
Cd = numpy.random.uniform(low = 20, high = 40, size = Q * M) # Shipping cost per unit of produced compost shipped from composting center q to compost customer m
 
Beta = 0.3 # Weight loss percentage in drying operations 
Omega = [0.4, 0.1, 0.5] #  Waste percentage of product type b from processing center j
yq = 0.6 # Production rate of compost from composting center q
ys = 2 # Production rate of cosmetic product from cosmetic factory s
yk = 1.01 # Production rate of pistachio factoy k
lambd = 0.4 # Waste percentage of oil extracting process in oil extraction center e

Cpa = numpy.random.uniform(low = 80000, high = 100000, size = I) # Production capacity for producer i
Cpu = numpy.random.uniform(low = 20000, high = 40000, size = J) # Production capacity for processing centers j
Cpy = numpy.random.uniform(low = 20000, high = 40000, size = Q) # Production capacity for composting center q
Cpw = numpy.random.uniform(low = 20000, high = 40000, size = K) # Production capacity for pistachio factory k
Cpr = numpy.random.uniform(low = 20000, high = 40000, size = E)  # Production capacity for oil extraction center e
Cpv = numpy.random.uniform(low = 20000, high = 40000, size = S) # Production capacity for cosmetic factory s
# CI = numpy.random.uniform(low = 20, high = 40, size = I)
Dc = numpy.random.uniform(low = 200, high = 400, size = M) # The demand for compost by customer M
Dp =  numpy.random.uniform(low = 200, high = 400, size = N1) # The demand of open-mouth pistachio by pistachio customer N1
Du =  numpy.random.uniform(low = 100, high = 200, size = N2) # The demand for oil by oil customer N2
Ds =  numpy.random.uniform(low = 20, high = 80, size = N3)#  The demand of cosmetic by cosmetic customer N3

numpy.savez_compressed("data.npz", I=I, K=K, J=J, E=E, Q=Q, S=S, N1=N1, N2=N2, N3=N3, M=M, Fu=Fu, Fy=Fy, Fw=Fw, Fr=Fr, Fv=Fv, CI=CI, Cy=Cy, Cw=Cw, Cr=Cr, Cv=Cv, Cu1=Cu1, Cu2=Cu2, CX=CX, CK=CK, CE=CE, CJ=CJ, CS=CS, CN=CN, CQ=CQ, Cl=Cl, Cp=Cp, Cd=Cd, Beta=Beta, Omega=Omega, yq=yq, ys=ys, yk=yk, lambd=lambd, Cpa=Cpa, Cpu=Cpu, Cpy=Cpy, Cpw=Cpw, Cpr=Cpr, Cpv=Cpv, Dc=Dc, Dp=Dp, Du=Du, Ds=Ds)