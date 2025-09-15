import numpy as np
import unittest
from Convergence import Convergence
from Solution import Solution

class ConvergenceTests(unittest.TestCase):
    def setUp(self):
        self.convergence = Convergence()

    def test_add(self):
        solution1 = Solution()
        solution1.FX = 0.5
        solution2 = Solution()
        solution2.FX = 0.3
        self.convergence.add(solution1)
        self.convergence.add(solution2)
        expected_convergence = np.array([0.5, 0.3])
        self.assertTrue(np.array_equal(self.convergence.get(), expected_convergence))

    def test_get(self):
        solution1 = Solution()
        solution1.FX = 0.5
        solution2 = Solution()
        solution2.FX = 0.3
        self.convergence.add(solution1)
        self.convergence.add(solution2)
        expected_convergence = np.array([0.5, 0.3])
        self.assertTrue(np.array_equal(self.convergence.get(), expected_convergence))

if __name__ == '__main__':
    unittest.main()