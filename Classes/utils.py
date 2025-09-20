import gdown
import numpy as np
from matplotlib import pyplot as plt

experiments = {
    "ga": {
        "url": "https://drive.google.com/drive/folders/1JtGIIawCR24ekgitUPFEXdAkMdrFn5Vf?usp=sharing",
        "path": "./experiments/ga/results/"
    },
    "global_optimum": {
        "url": "https://drive.google.com/drive/folders/1ypQsgn7fXAmCcELoqufUKHu2dD4IRzVG?usp=sharing",
        "path": "./experiments/global_optimum/solutions/"
    },
    "ils": {
        "url": "https://drive.google.com/drive/folders/1qrXqFoaGQlQ3zYSygXTky23fQuimwKIl?usp=sharing",
        "path": "./experiments/ils/results/"
    },
    "initialguess": {
        "url": "https://drive.google.com/drive/folders/1Vl7D3H1jiLlQWUePZHDoLcbzRPW-GTSr?usp=sharing",
        "path": "./experiments/initialguess/results/"
    },
    "vns": {
        "url": "https://drive.google.com/drive/folders/1gxkWFLX_Gzwmg_cmp3isb56VZK5iPOyw?usp=sharing",
        "path": "./experiments/vns/results/"
    }
}

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

def boxplot_fx(results, names):
    num_algorithms = len(results)
    num_executions = len(results[0][0])

    fx = np.zeros((num_algorithms, num_executions))
    for i in range(num_algorithms):
        for j in range(num_executions):
            fx[i, j] = results[i][0][j].FX

    plt.boxplot(fx.T, notch=True, patch_artist=True, boxprops=dict(facecolor='lightblue'))
    plt.xticks(np.arange(1, num_algorithms + 1), names, rotation=45)
    plt.ylabel(r"$f(x)$")
    plt.title("Objective Function Values")
    plt.tight_layout()
    plt.grid(axis='y')
    plt.show()

if __name__ == "__main__":
    loadResults("vns", quiet=False)