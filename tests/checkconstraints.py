"""
Constraint Validation Script for Pistachio Supply Chain Optimization

This script tests the constraint validation functionality of the optimization system
by generating a stochastic solution for a given problem instance and checking its
feasibility against all problem constraints.

Purpose:
    - Generate a random solution using stochastic chromosome generation
    - Evaluate the solution's objective function value
    - Validate all constraints to ensure solution feasibility
    - Report constraint violations and objective function value

Usage:
    python checkconstraints.py

"""

import sys
sys.path.append('Classes')

from Classes.Solution import Solution
from Classes.Problem import loadInstance

def main():
    """
    Main function to test constraint validation for a supply chain solution.
    
    This function:
    1. Loads a problem instance with 1600 data points
    2. Generates a stochastic solution
    3. Evaluates the solution's objective function
    4. Checks constraint feasibility
    5. Reports results
    """
    
    # Load problem instance
    print("Loading problem instance: data_1600")
    problem = loadInstance("data_1600", quiet=True)
    
    # Create and generate a stochastic solution
    print("Generating stochastic solution...")
    solution = Solution()
    solution.generateChromosomeStochastic(problem)
    
    # Evaluate the solution's objective function
    print("Evaluating solution...")
    fx = solution.evaluate(problem)
    
    # Check if solution is feasible
    if fx == float('inf'):
        print("❌ Solution is infeasible (FX = infinity)")
    else:
        print("✓ Solution is feasible")
    
    # Perform detailed constraint checking
    print("\nPerforming detailed constraint validation...")
    solution.check(problem)
    
    # Report final objective function value
    print(f"\nFinal Objective Function Value (FX): {solution.FX}")

if __name__ == "__main__":
    main()
