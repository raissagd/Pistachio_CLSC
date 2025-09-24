from numba import jit
import numpy as np
import time

@jit(nopython=True, cache=True)
def decodingStep_jit(v, a, b, c):
    """
    Step of the decoding process.

    Args:
        v (array): Chromosome (K+J)
        a (array): Capacity of source k
        b (array): Demand on depot j
        c (matrix): transportation cost of one unit of product from
        source k to depot j.
    """
    K, J = a.size, b.size  # K = number of sources, J = number of depots
    a, b, v = a.copy(), b.copy(), v.copy()

    # The amount of product shipped from source k to depot j
    g = np.zeros((K, J))

    # Iteration counter
    it = 0

    # Array to track active nodes (sources and depots)
    # 1 if active, 0 if not
    active = np.zeros(K + J)

    while True:
        # Select a node
        l = np.argmax(v)  # Select the node with the highest value

        # Mark the selected node as active
        active[l] = 1

        if l < K:  # Select a source
            k = l
            possible_depots = np.nonzero(v[K:])[0]
            j = possible_depots[np.argmin(c[k, possible_depots].flatten())]
        else:  # Select a depot
            j = l-K
            possible_sources = np.nonzero(v[:K])[0]
            k = possible_sources[np.argmin(c[possible_sources, j].flatten())]

        # Assign available amount of units
        g[k, j] = np.minimum(a[k], b[j])

        # Update availabilities on source k and depot j
        a[k] -= g[k, j]
        b[j] -= g[k, j]

        if a[k] == 0:
            v[k] = 0
        if b[j] == 0:
            v[K + j] = 0

        it += 1

        if np.all(v[K:] == 0) or np.sum(a) == 0:
            break

    # Calculate transportation cost
    cost = np.sum(g*c)

    return cost, g, active

def decodingStep_normal(v, a, b, c):
    """
    Step of the decoding process.

    Args:
        v (array): Chromosome (K+J)
        a (array): Capacity of source k
        b (array): Demand on depot j
        c (matrix): transportation cost of one unit of product from
        source k to depot j.
    """
    K, J = a.size, b.size  # K = number of sources, J = number of depots
    a, b, v = a.copy(), b.copy(), v.copy()

    # The amount of product shipped from source k to depot j
    g = np.zeros((K, J))

    # Iteration counter
    it = 0

    # Array to track active nodes (sources and depots)
    # 1 if active, 0 if not
    active = np.zeros(K + J)

    while True:
        # Select a node
        l = np.argmax(v)  # Select the node with the highest value

        # Mark the selected node as active
        active[l] = 1

        if l < K:  # Select a source
            k = l
            possible_depots = np.nonzero(v[K:])[0]
            j = possible_depots[np.argmin(c[k, possible_depots].flatten())]
        else:  # Select a depot
            j = l-K
            possible_sources = np.nonzero(v[:K])[0]
            k = possible_sources[np.argmin(c[possible_sources, j].flatten())]

        # Assign available amount of units
        g[k, j] = np.minimum(a[k], b[j])

        # Update availabilities on source k and depot j
        a[k] -= g[k, j]
        b[j] -= g[k, j]

        if a[k] == 0:
            v[k] = 0
        if b[j] == 0:
            v[K + j] = 0

        it += 1

        if np.all(v[K:] == 0) or np.sum(a) == 0:
            break

    # Calculate transportation cost
    cost = np.sum(g*c)

    return cost, g, active

# Test data
K, J = 20, 16
v = np.random.rand(K + J)
a = np.random.randint(10, 100, K).astype(float)
b = np.random.randint(10, 100, J).astype(float)
c = np.random.rand(K, J) * 10

# First run 
start_time = time.time()
decodingStep_jit(v, a, b, c)
jit_time = time.time() - start_time
start_time = time.time()
decodingStep_normal(v, a, b, c)
normal_time = time.time() - start_time

# Print first run times
print(f"First run - JIT version: {jit_time:.4f} seconds")
print(f"First run - Normal version: {normal_time:.4f} seconds")

# Number of iterations for timing
n_iterations = 20

# Time the JIT compiled version
start_time = time.time()
for _ in range(n_iterations):
    decodingStep_jit(v, a, b, c)
jit_time = time.time() - start_time

# Time the normal version
start_time = time.time()
for _ in range(n_iterations):
    decodingStep_normal(v, a, b, c)
normal_time = time.time() - start_time

print(f"JIT version: {jit_time:.4f} seconds")
print(f"Normal version: {normal_time:.4f} seconds")
print(f"Speedup: {normal_time/jit_time:.2f}x")