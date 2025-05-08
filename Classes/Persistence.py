"""
This module provides classes for persisting solution objects to disk 
using pickle serialization.

Classes:
    PersistSingleSolution: Handles the persistence of a single solution 
    object, allowing it to be saved to or loaded from a file.
    PersistMultipleSolutions: (incomplete) Intended to handle the 
    persistence of multiple solution objects.

The `PersistSingleSolution` class supports saving a solution object to a 
file and loading it back into memory. It uses the `.pkl` file format for 
serialization and deserialization of the solution object with the pickle 
module. This class can be useful in scenarios where solution states need 
to be preserved between program executions, such as caching results or 
intermediate states in computational pipelines.

The `PersistMultipleSolutions` class is intended to extend this 
functionality to handle multiple solution objects, although its 
implementation is not provided in the excerpt.

Example:
    To save a solution object:
        persister = PersistSingleSolution()
        persister.save(solution=my_solution, filename='solution1', 
        filepath='/path/to/save/')

    To load a solution object:
        loaded_solution = persister.load(filename='solution1', 
        filepath='/path/to/save/')
"""
import pickle

class PersistSingleSolution:
    """
    A class for persisting a single solution object.

    Attributes:
        format (str): The file format for saving the solution object.

    Methods:
        save: Save the solution object to a file.
        load: Load the solution object from a file.
    """

    def __init__(self) -> None:
        self.format = '.pkl'

    def save(self, solution=None, filename='', filepath=''):
        """
        Save the solution object to a file.

        Args:
            solution: The solution object to be saved.
            filename (str): The name of the file.
            filepath (str): The path where the file will be saved.
        """
        with open(filepath + filename + self.format, 'wb') as file:
            pickle.dump(solution, file)

    def load(self, filename='', filepath=''):
        """
        Load the solution object from a file.

        Args:
            filename (str): The name of the file.
            filepath (str): The path where the file is located.

        Returns:
            The loaded solution object.
        """
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

    def save(self, solutions=None, filename='', filepath='', log=True):
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
        
        # Only attempt to save logs if log parameter is True
        if log:
            try:
                for i in range(len(solutions)):
                    for j in range(len(solutions[i])):
                        for k in range(len(solutions[i][j])):
                            # Check if the solution object has a log attribute
                            if hasattr(solutions[i][j][k], 'log') and solutions[i][j][k].log is not None:
                                solutions[i][j][k].log.save(f"VNS{i}_Execution{k}", filepath)
            except (AttributeError, IndexError, TypeError) as e:
                print(f"Warning: Could not save log files. Error: {e}")

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