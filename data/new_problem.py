import sys
sys.path.append(r'C:\Users\Lenovo\Documents\IC')
from Classes.Problem import Problem

def createProblem(I, J, K, E, Q, S, N1, N2, N3, M, problem_size):
    problem = Problem()
    problem.generate(I, J, K, E, Q, S, N1, N2, N3, M)
    filename = f"data/data_{problem_size}.npz"
    problem.saveFile(filename)

I, J, K, E, Q, S, N1, N2, N3, M = 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600

createProblem(I, J, K, E, Q, S, N1, N2, N3, M, 1600)