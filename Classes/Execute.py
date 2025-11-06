from joblib import Parallel, delayed
from Persistence import PersistMultipleSolutions
from Algorithm import IteratedLocalSearch, GeneticAlgorithm
from Log import Neighborhood_op_log

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

    def run(self, data=None, method=None, number_times=30, log=True, show_progress=True):
        """
        Runs the specified method multiple times.

        Args:
            data: The input data for the method. Default is None.
            method: The method to be executed. Default is None.
            number_times: The number of times to run the method. Default is 30.
            show_progress: Whether to show progress information. Default is True.

        Returns:
            A list of results from running the method multiple times.
        """
        if show_progress:
            method_name = getattr(method.__class__, '__name__', str(method))
            print(f"Executing {method_name} {number_times} times...")
        
        if (isinstance(method, IteratedLocalSearch)
            or isinstance(method, GeneticAlgorithm)):
            results = Parallel(n_jobs=-1)(
                delayed(method.solve)(data, quiet=True) 
                for n in range(number_times)
            )
        else:
            if log:
                logs = [Neighborhood_op_log() for _ in range(number_times)]
            else:
                logs = [None for _ in range(number_times)]
            results = Parallel(n_jobs=-1)(
                delayed(method.solve)(data, log=logs[n], quiet=True) 
                for n in range(number_times)
            )
        
        if show_progress:
            print(f"✓ {method_name} finished ({number_times} executions)")
        
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

    def run(self, data=None, methods=None, number_times=30, pre_save=True, filename='', log=True, show_progress=True):
        """
        Runs multiple methods multiple times on a given problem.

        Args:
            data: The problem to be solved. Default is None.
            methods: The list of methods to be executed. Default is None.
            number_times: The number of times each method should be executed. Default is 30.
            show_progress: Whether to show progress information. Default is True.

        Returns:
            A list of results for each method.

        """
        results = []
        if pre_save:
            saving = PersistMultipleSolutions()
        
        if show_progress:
            print(f"Starting execution of {len(methods)} methods, {number_times} times each")
            print("=" * 60)
        
        for i, method in enumerate(methods):
            if show_progress:
                method_name = getattr(method.__class__, '__name__', str(method))
                print(f"[{i+1}/{len(methods)}] Method: {method_name}")
            results.append([])
            results[-1].append(RunSingleMethodMultipleTimes().run(
                data=data, method=method, number_times=number_times, log=log, show_progress=show_progress)
            )
            if pre_save:
                saving.save(solutions=results, filename=filename)
                if show_progress:
                    print(f"  ✓ Results saved to {filename}")
            
            if show_progress:
                print(f"  Overall progress: {i+1}/{len(methods)} methods completed")
                print("-" * 40)
                
        if show_progress:
            print(" All executions completed!")

        return results
    
    def resume(self, data=None, methods=None, number_times=30, results=None, pre_save=True, filename='', log=True, show_progress=True):
        """
        Resumes the execution of methods on the given data.

        Args:
            data: The input data to be used for execution.
            methods: A list of methods to be executed.
            number_times: The number of times each method should be executed.
            results: A list to store the results of each method execution.
            pre_save: A flag indicating whether to save the results before each execution.
            filename: The name of the file to save the results.
            show_progress: Whether to show progress information. Default is True.

        Returns:
            The updated results list after executing the methods.

        """
        M = len(results)
        if pre_save:
            saving = PersistMultipleSolutions()
        
        remaining_methods = len(methods) - M
        if show_progress:
            print(f"Resuming execution: {remaining_methods} methods remaining out of {len(methods)} total")
            print("=" * 60)
        
        for n in range(M, len(methods)):
            method = methods[n]
            if show_progress:
                method_name = getattr(method.__class__, '__name__', str(method))
                print(f"[{n+1}/{len(methods)}] Method: {method_name}")
            results.append([])
            results[n].append(RunSingleMethodMultipleTimes().run(
                data=data, method=method, number_times=number_times, log=log, show_progress=show_progress)
            )
            if pre_save:
                saving.save(solutions=results, filename=filename)
                if show_progress:
                    print(f"  ✓ Results saved to {filename}")
            
            if show_progress:
                print(f"  Overall progress: {n+1}/{len(methods)} methods completed")
                print("-" * 40)
        
        if show_progress:
            print(" Resumed execution completed!")
        
        return results
