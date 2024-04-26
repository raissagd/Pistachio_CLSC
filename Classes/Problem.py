import numpy as np

class Problem:

    def __init__(self):
        pass
    
    def generate(self, I, J, K, E, Q, S, N1, N2, N3, M):
        """
        Generate problem data.

        Args:
        - I (int): Number of producers.
        - J (int): Number of  processing centers.
        - K (int): Number of pistachio factories.
        - E (int): Number of  oil extraction centers.
        - Q (int): Number of composting centers.
        - S (int): Number of cosmetic factories.
        - N1 (int): Number of pistachio customers
        - N2 (int): Number of oil customers.
        - N3 (int): Number of cosmetic customers.
        - M (int): Number of compost customers.
        """
        self.I = I
        self.J = J
        self.K = K
        self.E = E
        self.Q = Q
        self.S = S
        self.N1 = N1
        self.N2 = N2
        self.N3 = N3
        self.M = M

        # Fixed costs
        self.Fu = np.random.uniform(low=20000, high=40000, size=self.J)
        self.Fy = np.random.uniform(low=10000, high=20000, size=self.Q)
        self.Fw = np.random.uniform(low=20000, high=50000, size=self.K)
        self.Fr = np.random.uniform(low=4000, high=8000, size=self.E)
        self.Fv = np.random.uniform(low=40000, high=80000, size=self.S)

        # Production costs
        self.CI = np.random.uniform(low=80, high=120, size=self.I)
        self.Cy = np.random.uniform(low=50, high=100, size=self.Q)
        self.Cw = np.random.uniform(low=100, high=150, size=self.K)
        self.Cr = np.random.uniform(low=40, high=80, size=self.E)
        self.Cv = np.random.uniform(low=150, high=180, size=self.S)
        self.Cu1 = np.random.uniform(low=60, high=100, size=self.J)
        self.Cu2 = np.random.uniform(low=80, high=120, size=self.J)

        # Shipping costs
        self.CX = np.random.uniform(low=20, high=40, size=(self.I, self.J))
        self.CK = np.random.uniform(low=20, high=40, size=(self.J, self.K))
        self.CE = np.random.uniform(low=20, high=40, size=(self.J, self.E))
        self.CJ = np.random.uniform(low=20, high=40, size=(self.J, self.Q))
        self.CS = np.random.uniform(low=20, high=40, size=(self.E, self.S))
        self.CN = np.random.uniform(low=20, high=40, size=(self.E, self.N2))
        self.CQ = np.random.uniform(low=20, high=40, size=(self.E, self.Q))
        self.Cl = np.random.uniform(low=20, high=40, size=(self.S, self.N3))
        self.Cp = np.random.uniform(low=20, high=40, size=(self.K, self.N1))
        self.Cd = np.random.uniform(low=20, high=40, size=(self.Q, self.M))

        # Parameters
        self.beta = 0.3
        self.theta = [0.4, 0.1, 0.5]
        self.gammaq = 0.6
        self.gammas = 2
        self.gammak = 1.01
        self.lamb = 0.4

        # Production capacities and demands
        self.Cpa = np.random.uniform(low=80000, high=100000, size=self.I)
        self.Cpu = np.random.uniform(low=20000, high=40000, size=self.J)
        self.Cpy = np.random.uniform(low=20000, high=40000, size=self.Q)
        self.Cpw = np.random.uniform(low=20000, high=40000, size=self.K)
        self.Cpr = np.random.uniform(low=20000, high=40000, size=self.E)
        self.Cpv = np.random.uniform(low=20000, high=40000, size=self.S)
        self.Dc = np.random.uniform(low=200, high=400, size=self.M)
        self.Dp = np.random.uniform(low=200, high=400, size=self.N1)
        self.Du = np.random.uniform(low=100, high=200, size=self.N2)
        self.Ds = np.random.uniform(low=20, high=80, size=self.N3)

    def saveFile(self, filename):
        """
        Save problem data to a compressed numpy file.

        Args:
        - filename: Name of the file to save.
        """
        np.savez_compressed(filename, I=self.I, K=self.K, J=self.J, E=self.E, Q=self.Q, S=self.S, N1=self.N1, N2=self.N2, N3=self.N3, M=self.M, 
                            Fu=self.Fu, Fy=self.Fy, Fw=self.Fw, Fr=self.Fr, Fv=self.Fv, CI=self.CI, Cy=self.Cy, Cw=self.Cw, Cr=self.Cr, 
                            Cv=self.Cv, Cu1=self.Cu1, Cu2=self.Cu2, CX=self.CX, CK=self.CK, CE=self.CE, CJ=self.CJ, CS=self.CS, CN=self.CN, 
                            CQ=self.CQ, Cl=self.Cl, Cp=self.Cp, Cd=self.Cd, beta=self.beta, theta=self.theta, gammaq=self.gammaq, gammas=self.gammas, 
                            gammak=self.gammak, lamb=self.lamb, Cpa=self.Cpa, Cpu=self.Cpu, Cpy=self.Cpy, Cpw=self.Cpw, Cpr=self.Cpr, Cpv=self.Cpv, 
                            Dc=self.Dc, Dp=self.Dp, Du=self.Du, Ds=self.Ds)

    def loadFile(self, filename):
        """
        Load problem data from a compressed numpy file.

        Args:
        - filename: Name of the file to load.
        """
        data = np.load(filename)

        # Assigning values to instance variables
        self.I, self.K, self.J, self.E, self.Q, self.S, self.N1, self.N2, self.N3, self.M = [data[variavel] for variavel in ["I", "K", "J", "E", "Q", "S", "N1", "N2", "N3", "M"]]
        self.Fu, self.Fy, self.Fw, self.Fr, self.Fv, self.CI, self.Cy, self.Cw, self.Cr, self.Cv, self.Cu1, self.Cu2, self.CX, self.CK, self.CE, self.CJ, self.CS, self.CN, self.CQ, self.Cl, self.Cp, self.Cd = [data[variavel] for variavel in ["Fu", "Fy", "Fw", "Fr", "Fv", "CI", "Cy", "Cw", "Cr", "Cv", "Cu1", "Cu2", "CX", "CK", "CE", "CJ", "CS", "CN", "CQ", "Cl", "Cp", "Cd"]]
        self.beta, self.theta, self.gammaq, self.gammas, self.gammak, self.lamb = [data[variavel] for variavel in ["beta", "theta", "gammaq", "gammas", "gammak", "lamb"]]
        self.Cpa, self.Cpu, self.Cpy, self.Cpw, self.Cpr, self.Cpv, self.Dc, self.Dp, self.Du, self.Ds = [data[variavel] for variavel in ["Cpa", "Cpu", "Cpy", "Cpw", "Cpr", "Cpv", "Dc", "Dp", "Du", "Ds"]]

        data.close()
