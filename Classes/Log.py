import pandas as pd
import os

class Log:
    """
    A base class for logging data into a Pandas DataFrame.
    """
    def __init__(self, columns):
        """
        Initializes the log with specified column names.
        
        Parameters:
        columns (list): A list of column names for the DataFrame.
        """
        self.columns = columns
        self.df = pd.DataFrame(columns=self.columns)  # Creating an empty DataFrame with given columns

    def log(self, data):
        """
        Adds a new entry to the log.
        
        Parameters:
        data (dict): A dictionary containing the data to be logged.
        """
        new_entry = pd.DataFrame([data])
    
        if self.df.empty:
            self.df = new_entry
        else:
            self.df = pd.concat([self.df, new_entry], ignore_index=True)

    def get(self):
        """
        Retrieves the current log as a DataFrame.
        
        Returns:
        pd.DataFrame: The stored log data.
        """
        return self.df
    

class Neighborhood_op_log(Log):
    """
    A specialized logging class for neighborhood operations in optimization algorithms.
    """
    def __init__(self):
        """
        Initializes the log with predefined column names for neighborhood operations.
        """
        columns = ["Instance", "Algorithm", "Operator", "Evaluations", "Success", "% Improvement", "FX"]
        super().__init__(columns)  # Calling the parent class constructor with predefined columns

    def log(self, instance, alg, operator, evaluations, success, improvement, FX):
        """
        Logs a neighborhood operation with specific attributes.
        
        Parameters:
        instance (str): The instance name.
        alg (str): The name of the algorithm used.
        operator (str): The neighborhood operator applied.
        evaluations (int): The number of evaluations performed.
        success (int): Indicator of success (1 for success, 0 for failure).
        improvement (float): Percentage of improvement achieved.
        """
        data = {
        "Instance": instance,
        "Algorithm": alg,
        "Operator": operator,
        "Evaluations": evaluations,
        "Success": success,
        "% Improvement": improvement,
        "FX": FX
        }
        return super().log(data)  # Calling the parent log method to store the data

    def save(self, filename, filepath):
        if not filename or not filepath:
            #print(f"[⚠️ Warning] Skipping log save due to missing filename or filepath.")
            return

        os.makedirs(filepath, exist_ok=True)
        full_path = os.path.join(filepath, filename + ".csv")
        #print(f"✅ Saving log to: {full_path}")
        self.df.to_csv(full_path, index=False)