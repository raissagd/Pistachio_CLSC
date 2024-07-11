from joblib import Parallel, delayed

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

    def run(self, data=None, methods=None, number_times=30):
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
        for method in methods:
            results.append(RunSingleMethodMultipleTimes().run(data=data, method=method, number_times=number_times))
        return results
