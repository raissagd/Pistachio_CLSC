import unittest
from Classes.Problem import Problem

class Problem_test(unittest.TestCase):

    def test_generate_vector_sizes(self):
        I, J, K, E, Q, S, N1, N2, N3, M = 5, 4, 3, 2, 6, 7, 8, 9, 10, 11
        problem = Problem()
        problem.generate(I, J, K, E, Q, S, N1, N2, N3, M)

        self.assertEqual(len(problem.Fu), J)
        self.assertEqual(len(problem.Fy), Q)
        self.assertEqual(len(problem.Fw), K)
        self.assertEqual(len(problem.Fr), E)
        self.assertEqual(len(problem.Fv), S)

        self.assertEqual(len(problem.CI), I)
        self.assertEqual(len(problem.Cy), Q)
        self.assertEqual(len(problem.Cw), K)
        self.assertEqual(len(problem.Cr), E)
        self.assertEqual(len(problem.Cv), S)
        self.assertEqual(len(problem.Cu1), J)
        self.assertEqual(len(problem.Cu2), J)

        self.assertEqual(problem.CX.shape, (I, J))
        self.assertEqual(problem.CK.shape, (J, K))
        self.assertEqual(problem.CE.shape, (J, E))
        self.assertEqual(problem.CJ.shape, (J, Q))
        self.assertEqual(problem.CS.shape, (E, S))
        self.assertEqual(problem.CN.shape, (E, N2))
        self.assertEqual(problem.CQ.shape, (E, Q))
        self.assertEqual(problem.Cl.shape, (S, N3))
        self.assertEqual(problem.Cp.shape, (K, N1))
        self.assertEqual(problem.Cd.shape, (Q, M))

        self.assertEqual(len(problem.Cpa), I)
        self.assertEqual(len(problem.Cpu), J)
        self.assertEqual(len(problem.Cpy), Q)
        self.assertEqual(len(problem.Cpw), K)
        self.assertEqual(len(problem.Cpr), E)
        self.assertEqual(len(problem.Cpv), S)
        self.assertEqual(len(problem.Dc), M)
        self.assertEqual(len(problem.Dp), N1)
        self.assertEqual(len(problem.Du), N2)
        self.assertEqual(len(problem.Ds), N3)

if __name__ == '__main__':
    unittest.main()