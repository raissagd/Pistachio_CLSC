import unittest
import os
from Persistence import PersistSingleSolution, PersistMultipleSolutions
from Solution import Solution
from Convergence import Convergence

class PersistSingleSolutionTests(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()
        self.solution.FX = 1.0
        for i in range(1, 9):
            setattr(self.solution, f'S{i}', [i])
        attributes = ['X', 'Go', 'Gr', 'Gw', 'O', 'Oc', 'Ow', 'L', 'P', 'D',
                      'U', 'Y', 'W', 'R', 'V']
        for i, attr in enumerate(attributes, 1):
            setattr(self.solution, attr, [i])
        self.solution.convergence = Convergence()
        self.solution.convergence.add(self.solution)
        self.filename = 'test_solution'
        self.filepath = ''

    def test_save_and_load(self):
        # Create an instance of SaveSolution
        save_solution = PersistSingleSolution()

        # Save the solution
        save_solution.save(self.solution, self.filename)

        # Load the solution
        loaded_solution = save_solution.load(self.filename)

        # Assert that the loaded solution is equal to the original solution
        self.assertEqual(loaded_solution, self.solution)

    def test_load_with_filepath(self):
        # Create an instance of SaveSolution
        save_solution = PersistSingleSolution()

        # Load the solution with filepath
        loaded_solution = save_solution.load(self.filename, self.filepath)

        # Assert that the loaded solution is equal to the original solution
        self.assertEqual(loaded_solution, self.solution)

class TestPersistMultipleSolutions(unittest.TestCase):
    def setUp(self):
        self.persistence = PersistMultipleSolutions()
        self.filename = 'test_solutions'
        self.filepath = './'
        self.solutions = []
        for i in range(3):
            solution = Solution()
            solution.FX = i
            for j in range(1, 9):
                setattr(solution, f'S{j}', [j])
            attributes = ['X', 'Go', 'Gr', 'Gw', 'O', 'Oc', 'Ow', 'L', 'P', 'D',
                          'U', 'Y', 'W', 'R', 'V']
            for j, attr in enumerate(attributes, 1):
                setattr(solution, attr, [j])
            self.solutions.append(solution)


    def tearDown(self):
        # Clean up the test file after each test
        file_path = self.filepath + self.filename + self.persistence.format
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_save_and_load(self):
        # Test saving and loading solutions
        solutions = ['solution1', 'solution2', 'solution3']
        self.persistence.save(solutions, self.filename, self.filepath)
        loaded_solutions = self.persistence.load(self.filename, self.filepath)
        self.assertEqual(solutions, loaded_solutions)

if __name__ == '__main__':
    unittest.main()