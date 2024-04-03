import numpy as np

class Solution:
    def __init__(self):
        self.FX = None # Objective function value
        self.S1, self.S2, self.S3, self.S4, self.S5, self.S6, self.S7, self.S8 = [None] * 8 # Chromosomes
        self.X, self.Go, self.Gr, self.Gw, self.O, self.Oc, self.Ow, self.L, self.P, self.D, self.U, self.Y, self.W, self.R, self.V = [None] * 15 # Decision variables
    
    def generateChromosome(self, data):
        """
        Generate an eight segment chromosome.

        Args:
        - I (int): Number of producers.
        - J (int): Number of processing centers.
        - K (int): Number of pistachio factories.
        - E (int): Number of oil extraction centers.
        - Q (int): Number of composting centers.
        - S (int): Number of cosmetic factories.
        - N1 (int): Number of pistachio customers
        - N2 (int): Number of oil customers.
        - N3 (int): Number of cosmetic customers.
        - M (int): Number of compost customers.
        """
        flows = [
            (data.K + data.N1),
            (data.S + data.N3),
            (data.E + data.N2 + data.S),
            (data.J + data.K),
            (data.J + data.E),
            (data.I + data.J),
            (data.Q + data.M),
            (data.J + data.E + data.Q)
        ]

        # Generate chromosomes for each flow and assign them to the corresponding attribute
        for i in range(1, 9):
            setattr(self, f"S{i}", np.random.permutation(np.arange(1, flows[i-1] + 1)))
    
    def decodingStep(self, v, a, b, c, show = False):
        """
        Step of the decoding process.

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
    
    def decode(self, data):
        """
        Decode the chromosome into a solution.

        Returns:
        - Decision variables: X ... V.
        """
        
        # Pistachio factories -> pistachio consumers

        # Source capacity
        a1 = data.gammak * data.Cpw  # amount coming from the processing center * factory production rate

        # Demand from each depot
        b1 = data.Dp

        # Total cost = transportation cost + production cost
        c1 = data.Cp + data.Cw[:, None]

        # Calculating cost and transportation matrix
        totalcost, self.P = self.decodingStep(self.S1, a1, b1, c1)

        # --------------------------------------------------------------------------------------------------------
        # Cosmetics factories -> cosmetics consumers
        a2 = data.gammas * data.Cpv
        b2 = data.Ds
        c2 = data.Cl + data.Cv[:, None]
        cost2, self.L = self.decodingStep(self.S2, a2, b2, c2)  # L = how much cosmetic was sent to each consumer
        totalcost += cost2

        # --------------------------------------------------------------------------------------------------------
        # Oil extraction centers -> oil consumers + cosmetics factories
        a3 = (1 - data.lamb) * data.Cpr  # oil extraction center production capacity x (1 - oil loss percentage in the extraction process)
        b3 = np.hstack((data.Du, np.sum(self.L, axis=1) / data.gammas))  # oil consumers demand + amount of oil that should be sent to cosmetics factories (amount calculated in the previous flow / factory production rate)
        c3 = np.hstack((data.CN + data.Cr[:, None], data.CS + data.Cr[:, None]))  # transportation cost from oil extraction center to oil consumer + transportation cost from oil extraction center to cosmetics factory
        cost3, OOc = self.decodingStep(self.S3, a3, b3, c3)  # OOc is an array with the amount of product that should be sent to each of the oil consumers and to the cosmetics factory (hence it needs to be split in two arrays)
        totalcost += cost3

        self.O = OOc[:, :data.N2]  
        self.Oc = OOc[:, data.N2:]  

        # --------------------------------------------------------------------------------------------------------
        # Processing center -> pistachio factories + oil extraction centers

        # Step 1: Processing center -> pistachio factories
        a4 = data.Cpu
        b4 = np.sum(self.P, axis=1) / data.gammak
        _, self.Go = self.decodingStep(self.S4, a4, b4, data.CK + data.Cu1[:, None])

        # --------------------------------
        # Step 2: Processing center -> oil extraction center
        a5 = data.Cpu
        b5 = (np.sum(self.O, axis=1) + np.sum(self.Oc, axis=1)) / (1 - data.lamb)
        _, self.Gr = self.decodingStep(self.S5, a5, b5, data.CE + data.Cu2[:, None])

        # --------------------------------
        # Step 3: enforcing equality constraints
        # Processing center demand compatible with transportation to pistachio factories
        bX1 = np.sum(self.Go, axis=1) / (1 - data.beta) / data.theta[0]

        # Processing center demand compatible with transportation to oil extraction center
        bX2 = np.sum(self.Gr, axis=1) / (1 - data.beta) / data.theta[1]

        # Final processing center demand
        b = np.zeros(data.J)

        # For each processing center
        for j in range(data.J):

            # If the demand related to pistachio factories is higher
            if bX1[j] > bX2[j]:

                # The final processing center demand is the demand related to pistachio factories
                b[j] = bX1[j]

                # Find which oil extraction center has the lowest cost
                e = np.argmin(data.CE[j, :] + data.Cu2[j])

                # Calculate how much raw kernel should leave the processing center
                amount = b[j] * data.theta[1] * (1 - data.beta)

                # Assign to that segment the amount of raw kernel needed to complete the final demand
                self.Gr[j, e] = self.Gr[j, e] + amount - np.sum(self.Gr[j, :])

            # Otherwise
            else:
                # The final processing center demand is the demand related to the oil extraction center
                b[j] = bX2[j]

                # Find which pistachio factory has the lowest cost
                k = np.argmin(data.CK[j, :] + data.Cu1[j])

                # Calculate how much open-mouth pistachio should leave the processing center
                amount = b[j] * data.theta[0] * (1 - data.beta)

                # Assign to that segment the amount of open-mouth pistachio needed to complete the final demand
                self.Go[j, k] = self.Go[j, k] + amount - np.sum(self.Go[j, :])

        # Calculate cost
        totalcost += np.sum((data.CK + data.Cu1[:, None]) * self.Go) + np.sum((data.CE + data.Cu2[:, None]) * self.Gr)

        # --------------------------------------------------------------------------------------------------------
        # Pistachio producers -> processing centers
        a6 = data.Cpa
        b6 = np.sum(self.Go, axis=1) / (1 - data.beta) / data.theta[0]
        c6 = data.CX + data.CI[:, None]
        cost6, self.X = self.decodingStep(self.S6, a6, b6, c6)
        totalcost += cost6

        # --------------------------------------------------------------------------------------------------------
        # Composting centers -> composting consumers
        a7 = data.gammaq * data.Cpy
        b7 = data.Dc
        c7 = data.Cd + data.Cy[:, None]
        cost7, self.D = self.decodingStep(self.S7, a7, b7, c7)
        totalcost += cost7

        # --------------------------------------------------------------------------------------------------------
        # Processing centers + oil extraction centers -> composting centers

        # Define the flow matrix between processing centers and composting centers
        self.Gw = np.zeros((data.J, data.Q))

        # The amount of waste to be sent by the processing centers
        a8 = np.sum(self.X, axis=0) * data.theta[2]

        # The minimum amount of waste needed by the composting centers
        b8 = np.sum(self.D, axis=1) / data.gammaq

        # For each processing center
        for j in range(data.J):
            # Identify the composting center with the lowest cost
            q = np.argmin(data.CJ[j, :])

            # Assign all the waste to that segment
            self.Gw[j, q] = a8[j]

        # For each composting center
        for q in range(data.Q):
            # If the amount of waste already sent is less than the required amount
            if b8[q] > self.Gw[:, q].sum():
                # Update the demand of the composting center by reducing the amount
                b8[q] = b8[q] - np.sum(self.Gw[:, q])

            # If the amount of waste already sent is greater than the required amount
            else:
                # No additional waste is needed
                b8[q] = 0

        # If there is still any composting center that needs waste
        if np.sum(b8) > 0:

            # Defining the capacity of each source
            a8 = data.lamb * np.sum(self.Gr, axis=0)

            # Calculating cost and transportation matrix
            _, self.Ow = self.decodingStep(self.S8, a8, b8, data.CQ)

        # Otherwise, it is not necessary to send any waste from the oil extraction center to the composting centers
        else:
            self.Ow = np.zeros((data.E, data.Q))

        # Update the costs
        totalcost += np.sum(data.CJ * self.Gw) + np.sum(data.CQ * self.Ow)
        
        # --------------------------------------------------------------------------------------------------------
        # Binary variables (opening of facilities)
        # Opening of processing centers
        u = np.sum(self.X, axis=0) != 0
        self.U = u.astype(int)

        # Opening of composting centers
        y = (self.Gw.sum(axis=0) + self.Ow.sum(axis=0)) != 0
        self.Y = y.astype(int)

        # Opening of pistachio factories
        w = np.sum(self.Go, axis=0) != 0
        self.W = w.astype(int)

        # Opening of oil extraction centers
        r = np.sum(self.Gr, axis=0) != 0
        self.R = r.astype(int)

        # Opening of cosmetics factories
        v = np.sum(self.Oc, axis=0) != 0
        self.V = v.astype(int)
        
        return totalcost
    
    def encode(self, n):
        pass
     
    def evaluate(self, data, show=False):
        """
        Evaluate a solution.

        Returns:
        - F1 (float): Objective function's total value.
        """
        
        totalcost = self.decode(data)
        
        # Objective function: transportation costs + production costs + opening costs
        F1 = totalcost + (np.sum(data.Fu * self.U) + np.sum(data.Fy * self.Y) + np.sum(data.Fw * self.W) + np.sum(data.Fr * self.R) 
              + np.sum(data.Fv * self.V))
        if show:
            print(f"The objective function = {totalcost}")
        
        self.FX = F1
        return F1
    
    
    def check(self, data):
        """
        Check if all restrictions have been respected.

        Returns:
        - valid (bool): True if the solution is valid, False otherwise.
        - failed_restrictions (list): List of restrictions that failed.
        """
                
        failed_restrictions = []
        equations = [
            (np.sum(self.X, axis=1), data.Cpa, "<=", "(1)"),
            (np.sum(self.X, axis=0), data.Cpu, "<=", "(2)"),
            (np.sum(self.Gw, axis=0) + np.sum(self.Ow, axis=0), data.Cpy, "<=", "(3)"),
            (np.sum(self.Go, axis=0), data.Cpw, "<=", "(4)"),
            (np.sum(self.Gr, axis=0), data.Cpr, "<=", "(5)"),
            (np.sum(self.Oc, axis=0), data.Cpv, "<=", "(6)"),
            (np.sum(self.Go, axis=1) + np.sum(self.Gr, axis=1) + np.sum(self.Gw, axis=1), np.sum(self.X, axis=0), "<=", "(7)"),
            (np.sum(self.Go, axis=1), (1-data.beta)*data.theta[0]*np.sum(self.X, axis=0), "==", "(8)"),
            (np.sum(self.Gr, axis=1), (1-data.beta)*data.theta[1]*np.sum(self.X, axis=0), "==", "(9)"),
            (np.sum(self.Gw, axis=1), data.theta[2]*np.sum(self.X, axis=0), "==", "(10)"),
            (np.sum(self.P, axis=1), data.gammak*np.sum(self.Go, axis=0), "<=", "(12)"),
            (np.sum(self.O, axis=1) + np.sum(self.Oc, axis=1), (1-data.lamb)*np.sum(self.Gr, axis=0), "<=", "(13)"),
            (np.sum(self.Ow, axis=1), data.lamb*np.sum(self.Gr, axis=0), "<=", "(14)"),
            (np.sum(self.L, axis=1), data.gammas*np.sum(self.Oc, axis=0), "<=", "(15)"),
            (np.sum(self.D, axis=1), data.gammaq*(np.sum(self.Gw, axis=0) + np.sum(self.Ow, axis=0)), "<=", "(16)"),
            (np.sum(self.P, axis=0), data.Dp, ">=", "(17)"),
            (np.sum(self.O, axis=0), data.Du, ">=", "(18)"),
            (np.sum(self.L, axis=0), data.Ds, ">=", "(19)"),
            (np.sum(self.D, axis=0), data.Dc, ">=", "(20)")
        ]

        for lhs, rhs, comparison, label in equations:
            if comparison == "<=":
                result = np.all(lhs <= rhs)
            elif comparison == "==":
                result = np.all(lhs == rhs)
            elif comparison == ">=":
                result = np.all(lhs >= rhs)
            else:
                raise ValueError("Invalid comparison operator")
                
            if not result and (comparison == "=="):
                failed_restrictions.append(f"Restriction {label} failed: {lhs} {comparison} {rhs}. Residual={np.abs(lhs-rhs)}")
            elif not result:
                failed_restrictions.append(f"Restriction {label} failed: {lhs} {comparison} {rhs}")

        if not failed_restrictions:
            print("All restrictions have been respected.")
            return True, None
        else:
            print("The following restrictions have been violated:")
            for restriction in failed_restrictions:
                print(restriction)
            return False, failed_restrictions