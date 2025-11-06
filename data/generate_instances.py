"""
Pistachio Closed Loop Supply Chain (CLSC) Instance Generator

This script generates problem instances of various sizes for testing and benchmarking
optimization algorithms in the Pistachio CLSC optimization framework.

The script creates instances with different problem sizes, where all node types in the
supply chain network have the same quantity. Each instance is saved as a compressed
NumPy file (.npz) for efficient storage and loading.
"""

import sys
sys.path.insert(0, 'Classes/')
from Problem import Problem


def createProblem(problem_size):
    """
    Create a problem instance with specified size for all network nodes.
    
    This function generates a complete supply chain network where all node types
    (producers, processing centers, factories, customers, etc.) have the same
    quantity equal to the problem_size parameter.
    
    Args:
        problem_size (int): The number of nodes for each type in the supply chain.
                           This value is used for all node types (I, J, K, E, Q, S, N1, N2, N3, M).
    
    Node Types:
        I:  Pistachio producers (initial suppliers)
        J:  Processing centers (first-level processing)
        K:  Pistachio factories (processed pistachio production)
        E:  Oil extraction centers (oil processing)
        Q:  Composting centers (waste processing)
        S:  Cosmetic factories (final products)
        N1: Pistachio customers
        N2: Oil customers
        N3: Cosmetic customers
        M:  Composting customers
    
    Output:
        Saves the generated instance to 'data/data_{problem_size}.npz'
    """
    # Set all node types to the same size
    I = J = K = E = Q = S = N1 = N2 = N3 = M = problem_size
    
    # Create and generate the problem instance
    problem = Problem()
    problem.generate(I, J, K, E, Q, S, N1, N2, N3, M)
    
    # Save the instance to a compressed NumPy file
    filename = f"data/data_{problem_size}.npz"
    problem.saveFile(filename)
    print(f"Generated instance: {filename}")


# Define the sizes of instances to generate
# These sizes provide a range from small test instances to large-scale problems
instance_sizes = [
    10,    # Small instance for quick testing
    30,    # Small-medium instance
    100,   # Medium instance
    200,   # Medium-large instance
    400,   # Large instance
    800,   # Very large instance
    1600   # Extra large instance for scalability testing
]

# Generate all instances
print("Generating Pistachio CLSC problem instances...")
print(f"Instance sizes: {instance_sizes}")
print("-" * 50)

for instance in instance_sizes:
    createProblem(instance)

print("-" * 50)
print(f"Successfully generated {len(instance_sizes)} problem instances!")
print("Files saved in 'data/' directory with format: data_{size}.npz")
