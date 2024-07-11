import pickle

class PersistSingleSolution:
    def __init__(self) -> None:
        self.format = '.pkl'
    def save(self, solution=None, filename='', filepath=''):
        with open(filepath + filename + self.format, 'wb') as file:
            pickle.dump(solution, file)
    def load(self, filename='', filepath=''):
        with open(filepath + filename + self.format, 'rb') as file:
            solution = pickle.load(file)
        return solution

class PersistMultipleSolutions:
    """
    A class for persisting multiple solutions using pickle serialization.

    Attributes:
        format (str): The file format for serialization.

    Methods:
        save: Save the solutions to a file.
        load: Load the solutions from a file.
    """

    def __init__(self) -> None:
        self.format = '.pkl'

    def save(self, solutions=None, filename='', filepath=''):
        """
        Save the solutions to a file.

        Args:
            solutions (object): The solutions to be saved.
            filename (str): The name of the file.
            filepath (str): The path to the file.

        Returns:
            None
        """
        with open(filepath + filename + self.format, 'wb') as file:
            pickle.dump(solutions, file)

    def load(self, filename='', filepath=''):
        """
        Load the solutions from a file.

        Args:
            filename (str): The name of the file.
            filepath (str): The path to the file.

        Returns:
            object: The loaded solutions.
        """
        with open(filepath + filename + self.format, 'rb') as file:
            solutions = pickle.load(file)
        return solutions