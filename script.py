from Problem import Problem
from Solution import Solution
from Neighbourhood import Swap

I, J, K, E, Q, S, N1, N2, N3, M = 3, 2, 1, 1, 1, 1, 2, 2, 1, 2

# Creating an instance of the Problem class
problem = Problem()
problem.generate(I, J, K, E, Q, S, N1, N2, N3, M)
problem.saveFile("data.npz")
data = Problem()
data.loadFile("data.npz")

# Creating an instance of the Solution class
solution = Solution()
solution.generateChromosome(I, J, K, E, Q, S, N1, N2, N3, M)
solution.evaluate(data)
solution.check(data)

print('--- Neighbourhood class test: ----')
test = Swap(solution)
test.move(2)
