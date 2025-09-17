# Experiments

## Global Optimum

* Goal: to obtain the global optimum solutions for each instance using Gurobi
* Instances 400, 800, and 1600: the global optimum is not possible
  - Memory overflow (Gurobi)
  - Initial guess provided by the deterministic initialization and Gurobi returns
    the best solution found before memory overflow (1000~1500 seconds)

## Initial Guess

* Goal: to compare deterministic initialization against stochastic one
* Algorithm: ILS (InactiveActiveSwap)
* Instance: 400

## ILS, VNS, GA

* Goal: to compare possible formulations among each algorithm and then to 
  compare the best algorithms.
* Instance: 400