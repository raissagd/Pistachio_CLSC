from joblib import Parallel, delayed
from Persistence import PersistMultipleSolutions

class RunSingleMethodMultipleTimes:
    """
    A class that runs a single method multiple times.

    Args:
        data: The input data for the method. Default is None.
        method: The method to be executed. Default is None.
        number_times: The number of times to run the method. Default is 30.

    Returns:
        A list of results from running the method multiple times.
    """

    def __init__(self) -> None:
        pass

    def run(self, data=None, method=None, number_times=30):
        """
        Runs the specified method multiple times.

        Args:
            data: The input data for the method. Default is None.
            method: The method to be executed. Default is None.
            number_times: The number of times to run the method. Default is 30.

        Returns:
            A list of results from running the method multiple times.
        """
        results = Parallel(n_jobs=-1)(delayed(method.solve)(data) for _ in range(number_times))
        return results

class RunMultipleMethodsMultipleTimes:
    """
    A class that runs multiple methods multiple times on a given problem.

    Args:
        data: The problem to be solved. Default is None.
        methods: The list of methods to be executed. Default is None.
        number_times: The number of times each method should be executed. Default is 30.

    Returns:
        A list of results for each method.

    """
    def __init__(self) -> None:
        pass

    def run(self, data=None, methods=None, number_times=30, pre_save=True,
            filename=''):
        """
        Runs multiple methods multiple times on a given problem.

        Args:
            data: The problem to be solved. Default is None.
            methods: The list of methods to be executed. Default is None.
            number_times: The number of times each method should be executed. Default is 30.

        Returns:
            A list of results for each method.

        """
        results = []
        n = 0
        if pre_save:
            saving = PersistMultipleSolutions()
        for method in methods:
            results.append([])
            results[n].append(RunSingleMethodMultipleTimes().run(
                data=data, method=method, number_times=number_times)
            )
            if pre_save:
                saving.save(solutions=results, filename=filename)
                
        return results
    
    def resume(self, data=None, methods=None, number_times=30, results=None,
               pre_save=True, filename=''):
        """
        Resumes the execution of methods on the given data.

        Args:
            data: The input data to be used for execution.
            methods: A list of methods to be executed.
            number_times: The number of times each method should be executed.
            results: A list to store the results of each method execution.
            pre_save: A flag indicating whether to save the results before each execution.
            filename: The name of the file to save the results.

        Returns:
            The updated results list after executing the methods.

        """
        M = len(results)
        if pre_save:
            saving = PersistMultipleSolutions()
        for n in range(M, len(methods)):
            method = methods[n]
            results.append([])
            results[n].append(RunSingleMethodMultipleTimes().run(
                data=data, method=method, number_times=number_times)
            )
            if pre_save:
                saving.save(solutions=results, filename=filename)
        return results
