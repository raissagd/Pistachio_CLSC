from Problem import Problem
from Solution import Solution

I, J, K, E, Q, S, N1, N2, N3, M = 3, 2, 1, 1, 1, 1, 2, 2, 1, 2

# Creating an instance of the Problem class
problem = Problem()
problem.generate(I, J, K, E, Q, S, N1, N2, N3, M)
problem.saveFile("data.npz")
data = Problem()
data.loadFile("data.npz")

# Creating an instance of the Solution class
solution = Solution()
S1, S2, S3, S4, S5, S6, S7, S8 = solution.generateChromosome(I, J, K, E, Q, S, N1, N2, N3, M)
X, Go, Gr, Gw, O, Oc, Ow, L, P, D, U, Y, W, R, V, totalcost = solution.decode(data, S1, S2, S3, S4, S5, S6, S7, S8)
solution.evaluate(data, U, Y, W, R, V, totalcost, show = True)
solution.check(data, X, Go, Gr, Gw, O, Oc, Ow, L, P, D)