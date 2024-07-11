import unittest
from Persistence import SaveSolution
from Solution import Solution
from Convergence import Convergence

class SaveSolutionTests(unittest.TestCase):
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
        save_solution = SaveSolution()

        # Save the solution
        save_solution.save(self.solution, self.filename)

        # Load the solution
        loaded_solution = save_solution.load(self.filename)

        # Assert that the loaded solution is equal to the original solution
        self.assertEqual(loaded_solution, self.solution)

    def test_load_with_filepath(self):
        # Create an instance of SaveSolution
        save_solution = SaveSolution()

        # Load the solution with filepath
        loaded_solution = save_solution.load(self.filename, self.filepath)

        # Assert that the loaded solution is equal to the original solution
        self.assertEqual(loaded_solution, self.solution)

if __name__ == '__main__':
    unittest.main()