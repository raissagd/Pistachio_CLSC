"""
This module contains the Convergence class, which is used to track the 
convergence of solutions.

Classes:
    Convergence: A class to track the convergence of solutions.

"""

import numpy as np

class Convergence:
    """
    A class to track the convergence of solutions.

    Attributes:
        convergence (list): A list to store the convergence values.

    Methods:
        add(solution): Adds a solution's convergence value to the list.
        get(): Returns the convergence values as a numpy array.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of the Convergence class.
        """
        self.convergence = []

    def add(self, solution):
        """
        Adds a solution's convergence value to the list.

        Args:
            solution: The solution object containing the convergence value.
        """
        self.convergence.append(solution.FX)

    def get(self):
        """
        Returns the convergence values as a numpy array.

        Returns:
            numpy.ndarray: The convergence values.
        """
        return np.array(self.convergence)
