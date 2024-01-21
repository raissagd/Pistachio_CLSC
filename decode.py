def decode_step(K, J, b, a, c, chromosome):
    g = 0  # Step 1: Initialize g to zero

    # Step 2: Find the index 'l' with the highest priority in the chromosome that is not zero.
    non_zero_priorities = [i for i, v in enumerate(chromosome) if v != 0]
    if not non_zero_priorities:
        # If all priorities are zero, the algorithm should terminate.
        return None, None, None, 0

    l = max(non_zero_priorities, key=lambda x: chromosome[x])

    # Step 3: Select the source or depot based on 'l'
    if l < len(K):  # 'l' is a source index
        k_star = K[l]
        eligible_depots = [j for j in J if chromosome[len(K) + j] != 0]
        if not eligible_depots:
            # No eligible depots left, terminate the algorithm
            return None, None, None, 0
        j_star = min(eligible_depots, key=lambda j: c[k_star][j])
    else:  # 'l' is a depot index
        j_star = J[l - len(K)]
        eligible_sources = [k for k in K if chromosome[k] != 0]
        if not eligible_sources:
            # No eligible sources left, terminate the algorithm
            return None, None, None, 0
        k_star = min(eligible_sources, key=lambda k: c[k][j_star])

    # Step 4: Assign the minimum available quantity from the source to the depot
    g = min(a[k_star], b[j_star])

    # Update the availabilities at the source and depot
    a[k_star] -= g
    b[j_star] -= g

    # Invalidate the exhausted source or depot in the chromosome
    if a[k_star] == 0:
        chromosome[k_star] = 0
    if b[j_star] == 0:
        chromosome[len(K) + j_star] = 0

    # Calculate the cost of the shipment
    cost = g * c[k_star][j_star]

    # Return the shipment quantity, source, depot, and cost
    return g, k_star, j_star, cost

def print_shipment_info(k_star, j_star, g, cost, chromosome, a, b):
    print(f"Source: {k_star + 1}")
    print(f"Depot: {j_star + 1}")
    print(f"Quantity: {g:.2f}")
    print(f"Cost: {cost:.2f}")
    print("Update chromosome:", chromosome)
    print("Updated sources' capacities:", a)
    print("Updated depots' demands:", b)
    print("---------------------------------------------------")

def decode(K, J, b, a, c, chromosome):
    total_cost = 0
    quantity_fabrication = [0 for _ in K]

    # Continue decoding the chromosome until all priorities are zero
    while any(v != 0 for v in chromosome):
        result = decode_step(K, J, b, a, c, chromosome)
        if result == (None, None, None, 0):
            break

        g, k_star, j_star, cost = result
        total_cost += cost  
        quantity_fabrication[k_star] += g 
        #print_shipment_info(k_star, j_star, g, cost, chromosome, a, b)

    #print(f"Total operation cost: {(total_cost):.2f}")
    #for i, fabrication in enumerate(quantity_fabrication):
        #print(f"Source {i + 1} needs to produce {(fabrication):.2f} to meet demand.")
