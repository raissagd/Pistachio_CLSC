import gdown

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

    # Google Drive folder URL containing the instances
    url = experiments[experiment_name].get("url")
    if url is None:
        raise ValueError(f"Experiment '{experiment_name}' not found in the "
                         "repository.")
    path = experiments[experiment_name].get("path")
    
    # Download the file from Google Drive
    gdown.download_folder(url, output=path, quiet=quiet, use_cookies=False)

if __name__ == "__main__":
    loadResults("vns", quiet=False)