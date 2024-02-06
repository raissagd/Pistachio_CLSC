import numpy as np

def decoding(v, a, b, c, show=False):
    """decoding

    Args:
        v (array): Chromosome (K+J)
        a (array): Capacity of source k
        b (array): Demand on depot j
        c (matrix): transportation cost of one unit of product from
        source k to depot j.
    """
    K, J = a.size, b.size
    a, b, v = a.copy(), b.copy(), v.copy()
        
    # The amount of product shipped from source k to depot j
    g = np.zeros((K, J))

    # Iteration counter
    it = 0
        
    while True:
        
        # Select a node
        l = np.argmax(v)
            
        if l < K: # Select a source
            k = l
            possible_depots = np.nonzero(v[K:])[0]
            # Select a depot with the lowest cost
            j = possible_depots[np.argmin(c[k, possible_depots].flatten())]
        else: # Select a depot
            j = l-K
            possible_sources = np.nonzero(v[:K])[0]
            k = possible_sources[np.argmin(c[possible_sources, j].flatten())]
        
        # Assign available amount of units
        g[k, j] = np.minimum(a[k], b[j])
        
        if show:
            print(f"it={it}, v={v}, a={a}, b={b}, k={k+1}, j={j+1}, g_kj={g[k, j]}")
        
        # Update availabilities on source k and depot j
        a[k] -= g[k, j]
        b[j] -= g[k, j]
            
        if a[k] == 0:
            v[k] = 0
        if b[j] == 0:
            v[K + j] = 0
            
        it += 1
            
        if np.all(v[K:] == 0):
            break

    if show:
        print(f"it={it}, v={v}, a={a}, b={b}, k={k+1}, j={j+1}, g_kj={g[k, j]}")
    
    # Calculate transportation cost
    cost = np.sum(g*c)
    
    return cost, g