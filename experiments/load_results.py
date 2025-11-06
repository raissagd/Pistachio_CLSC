import sys
sys.path.append("./Classes/")
from utils import loadResults, experiments

for experiment in experiments.keys():
    print(f"Loading results for experiment: {experiment}")
    loadResults(experiment, quiet=False)
print("All results loaded.")