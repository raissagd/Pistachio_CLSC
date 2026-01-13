import gdown
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl

experiments = {
    "ga": {
        "url": "https://drive.google.com/drive/folders/1W2dyeRBuXaMGftWrMvS2imQ70m0LgpjN?usp=sharing",
        "path": "./experiments/ga/"
    },
    "global_optimum": {
        "url": "https://drive.google.com/drive/folders/1aUhDU_FN7-71tPZ0CjSXinjT2e-zB0P_?usp=sharing",
        "path": "./experiments/global_optimum/"
    },
    "ils": {
        "url": "https://drive.google.com/drive/folders/1DX9kyKt300vvX1UuP5EJbHSFGid2UCyF?usp=sharing",
        "path": "./experiments/ils/"
    },
    "initialguess": {
        "url": "https://drive.google.com/drive/folders/1LAROm94ymyugha8CBQBDdGCTg9ohCr5P?usp=sharing",
        "path": "./experiments/initialguess/"
    },
    "vns": {
        "url": "https://drive.google.com/drive/folders/14I21lkQkxph4iA75i8ZrsC6C3cgX-qZ-?usp=sharing",
        "path": "./experiments/vns/"
    }
}

# Configurando globalmente
plt.rcParams['font.size'] = 18  # Tamanho base
plt.rcParams['axes.labelsize'] = 18  # Labels dos eixos
plt.rcParams['axes.titlesize'] = 18  # Títulos
plt.rcParams['legend.fontsize'] = 18  # Legenda
plt.rcParams['xtick.labelsize'] = 16  # Números eixo x
plt.rcParams['ytick.labelsize'] = 18  # Números eixo y

def loadResults(experiment_name, quiet=False):
    """
    Load results from a Google Drive folder for a specified experiment.
    This function downloads experiment results from a Google Drive folder URL
    associated with the given experiment name. The experiment configuration
    must be defined in the experiments dictionary with 'url' and 'path' keys.
    Parameters
    ----------
    experiment_name : str
        The name of the experiment to load results for. Must be a key in the
        experiments dictionary.
    quiet : bool, optional
        If True, suppresses download progress output. Default is False.
    Raises
    ------
    ValueError
        If the experiment_name is not found in the experiments repository
        or if the experiment configuration is missing required fields.
    Notes
    -----
    This function requires the gdown library to be installed and uses
    gdown.download_folder() to download the entire folder structure
    from Google Drive without using cookies.
    """

    # Google Drive folder URL containing the instances
    url = experiments[experiment_name].get("url")
    if url is None:
        raise ValueError(f"Experiment '{experiment_name}' not found in the "
                         "repository.")
    path = experiments[experiment_name].get("path")
    
    # Download the file from Google Drive
    gdown.download_folder(url, output=path, quiet=quiet, use_cookies=False)

def get_fx_samples(results):
    """
    Extract objective function values (FX) from a nested results structure.
    This function processes a nested list of results, where each result object
    is expected to have an 'FX' attribute. It extracts these FX values and
    organizes them into a 2D NumPy array for further analysis.
    Parameters
    ----------
    results : list of list of objects
        A nested list where results[i][0][j] contains optimization result objects.
        The structure is: [algorithm][metric][execution], where each result object
        must have an 'FX' attribute containing the objective function value.
    Returns
    -------
    numpy.ndarray
        A 2D array of shape (num_algorithms, num_executions) containing the FX
        values extracted from the results.
    Notes
    -----
    - The function assumes all algorithms have the same number of execution runs.
    - Each result object must have an 'FX' attribute accessible via dot notation.
    """
    num_algorithms = len(results)
    num_executions = len(results[0][0])

    fx = np.zeros((num_algorithms, num_executions))
    for i in range(num_algorithms):
        for j in range(num_executions):
            fx[i, j] = results[i][0][j].FX

    return fx

def boxplot_fx(results, names, global_optimum=None):
    """
    Generate a boxplot visualization of objective function values across multiple algorithms and executions.
    This function creates a boxplot showing the distribution of objective function values (FX)
    for different optimization algorithms across multiple execution runs. Each box represents
    the statistical distribution of results for one algorithm.
    Parameters
    ----------
    results : list of list of objects
        A nested list where results[i][0][j] contains optimization result objects.
        The structure is: [algorithm][metric][execution], where each result object
        must have an 'FX' attribute containing the objective function value.
    names : list of str
        Names of the algorithms corresponding to each algorithm in results.
        Used as x-axis labels in the boxplot.
    global_optimum : object, optional
        An object with an 'FX' attribute representing the known global optimum value.
        If provided, a horizontal dashed red line will be drawn at this value.
        Default is None.
    Returns
    -------
    None
        The function displays the plot using matplotlib.pyplot.show().
    Notes
    -----
    - The function assumes all algorithms have the same number of execution runs
    - Each result object must have an 'FX' attribute accessible via dot notation
    - The plot includes a grid on the y-axis for better readability
    - Algorithm names on x-axis are rotated 45 degrees to prevent overlap
    """
    num_algorithms = len(results)
    fx = get_fx_samples(results)

    plt.boxplot(fx.T, notch=True, patch_artist=True,
                boxprops=dict(facecolor='lightblue'))
    
    if global_optimum is not None:
        plt.axhline(global_optimum.FX, color='red', linestyle='--', 
                    label='Global Optimum')
        plt.legend()
    plt.xticks(np.arange(1, num_algorithms + 1), names, rotation=45)
    plt.ylabel(r"$f(x)$")
    plt.title("Objective Function Values")
    plt.tight_layout()
    plt.grid(axis='y')
    plt.show()


def _compute_boxes(solutions, num_slots=8):
    """
    Compute interpolated convergence data for boxplot visualization.
    This function processes solution convergence data by normalizing execution percentages
    and interpolating function values across uniform slots for statistical analysis.
    Args:
        solutions (list): List containing solution objects where solutions[0] contains
                         execution results with convergence data accessible via
                         .convergence.get() method.
        num_slots (int, optional): Number of interpolation slots to create along
                                 the convergence curve. Defaults to 8.
    Returns:
        tuple: A tuple containing:
            - nfx (numpy.ndarray): 2D array of shape (num_executions, num_slots+1)
                                  containing interpolated function values for each execution.
            - slots (numpy.ndarray): 1D array of interpolation points from 0 to 1.
            - medians (numpy.ndarray): 1D array of median values across all executions
                                     for each slot position.
    Note:
        The function assumes that convergence data returns a tuple where the first
        element represents iteration/evaluation counts and the second element
        represents corresponding function values.
    """
    num_executions = len(solutions[0])
    percentage = [None] * num_executions
    fx = [None] * num_executions

    for j in range(num_executions):
        convergence = solutions[0][j].convergence.get()
        percentage[j] = convergence[0]/max(convergence[0])
        fx[j] = convergence[1]

    slots = np.linspace(0, 1, num_slots+1)
    nfx = np.zeros((num_executions, len(slots)))
    for i in range(num_executions):
        nfx[i, :] = np.interp(slots, percentage[i], fx[i])

    medians = np.median(nfx, axis=0)

    return nfx, slots, medians

def boxplot_convergence(solutions, names):
    """
    Create boxplot visualizations showing convergence patterns for multiple optimization solutions.
    This function generates a series of boxplots that display the distribution of objective 
    function values across different stages of the optimization process. Each solution gets 
    its own subplot with boxplots showing the quartiles and medians at various execution 
    percentages, along with a median line connecting the boxes.
    Parameters
    ----------
    solutions : list
        A list of solution data structures, where each element contains optimization 
        results that can be processed by the _compute_boxes function.
    names : list of str
        A list of names/labels for each solution, used for subplot titles and legends. 
        Must have the same length as solutions.
    Returns
    -------
    None
        The function displays the plot using plt.show() and does not return any value.
    Notes
    -----
    - The function creates subplots with shared y-axis for easy comparison
    - Uses 8 slots by default to divide the execution into percentage intervals
    - Each solution is assigned a different color from the 'tab10' colormap
    - The x-axis represents the percentage of execution (0-100%)
    - The y-axis shows objective function values
    - Boxplots show quartiles while the connected line shows median progression
    Dependencies
    ------------
    Requires matplotlib.pyplot, numpy, and a helper function _compute_boxes that 
    processes the solution data into boxplot-ready format.
    """
    # Define colors for different solutions
    colors = mpl.color_sequences['tab10']

    # Create subplots with shared y-axis
    fig, axes = plt.subplots(1, len(solutions), figsize=(6*len(solutions), 5), 
                             sharey=True)

    # Handle case where there's only one solution (axes won't be a list)
    if len(solutions) == 1:
        axes = [axes]

    for i in range(len(solutions)):
        nfx, slots, medians = _compute_boxes(solutions[i], num_slots=8)
        
        axes[i].boxplot(nfx, positions=np.linspace(0, 100, len(slots)), widths=8,
                        patch_artist=True, boxprops=dict(facecolor=colors[i]), 
                        medianprops=dict(color=colors[i]))
        axes[i].plot(np.linspace(0, 100, len(slots)), medians, color=colors[i], 
                    linewidth=2, label=names[i])
        axes[i].set_xlabel("Percentage of the execution")
        axes[i].set_title(names[i])
        axes[i].grid(True, which="both", ls="--")

    # Only set ylabel for the first subplot
    axes[0].set_ylabel("Objective function value")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    loadResults("vns", quiet=False)