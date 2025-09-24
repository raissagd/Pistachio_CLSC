import numpy as np
from scipy.sparse import csr_matrix
from numba import jit

class Solution:
    def __init__(self):
        self.FX = float('inf')  # Objective function value (start with high value)
        self.S1, self.S2, self.S3, self.S4, self.S5, self.S6, self.S7, self.S8 = [None] * 8  # Chromosomes
        self.A1, self.A2, self.A3, self.A4, self.A5, self.A6, self.A7, self.A8 = [None] * 8  # Active nodes
        self.X, self.Go, self.Gr, self.Gw, self.O, self.Oc, self.Ow, self.L, self.P, self.D, self.U, self.Y, self.W, self.R, self.V = [None] * 15  # Decision variables
        self.convergence = None  # Convergence curve
        self.n_eval = 0
        self.execution_time = 0.0  # Execution time
        self.log = None  # Log for operations

    def calculate_priorities(self, transportation_matrix):
        """
        Generate a chromosome based on the mean costs of the transportation matrix.
        """
        row_means = np.mean(transportation_matrix,
                            axis=1)  # Calculate mean of each row
        # Calculate mean of each column
        col_means = np.mean(transportation_matrix, axis=0)
        # Concatenate row and column means
        means_array = np.concatenate((row_means, col_means))
        # Create an array of numbers from 1 to len(means_array)
        priority_array = np.arange(1, len(means_array) + 1)

        # Sort the means_array along with their indices
        sorted_indices = np.argsort(means_array)
        sorted_means = means_array[sorted_indices]

        # Assign priorities to each value in means_array
        current_priority = 1
        for i in range(len(sorted_means)):
            if i > 0 and sorted_means[i] == sorted_means[i - 1]:
                # If the current value is equal to the previous one, assign the next sequential priority
                current_priority += 1
            else:
                # Otherwise, assign a new priority
                # Ensure sequential priorities
                current_priority = max(current_priority, i + 1)
            priority_array[sorted_indices[i]] = current_priority

        return priority_array

    def generateChromosomeDeterministic(self, data):
        """
        Generate an eight segment chromosome.

        S1: Pistachio factories -> pistachio consumers (K + N1)
        S2: Cosmetics factories -> cosmetics consumers (S + N3)
        S3: Oil extraction centers -> oil consumers + cosmetics factories (E + N2 + S)
        S4: Processing center -> pistachio factories (J + K)
        S5: Processing center -> oil extraction center (J + E)
        S6: Pistachio producers -> processing centers (I + J)
        S7: Composting centers -> composting consumers (Q + M)
        S8: Oil extraction centers -> composting centers (E + Q)
        """
        self.S1 = self.calculate_priorities(data.Cp)
        self.S2 = self.calculate_priorities(data.Cl)
        self.S3 = self.calculate_priorities(np.hstack((data.CN, data.CS)))
        self.S4 = self.calculate_priorities(data.CK)
        self.S5 = self.calculate_priorities(data.CE)
        self.S6 = self.calculate_priorities(data.CX)
        self.S7 = self.calculate_priorities(data.Cd)
        self.S8 = self.calculate_priorities(data.CQ)

    def generateChromosomeStochastic(self, data):
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
            # (data.J + data.E + data.Q)
            (data.E + data.Q)
        ]

        # Generate chromosomes for each flow and assign them to the corresponding attribute
        for i in range(1, 9):
            setattr(self, f"S{i}", np.random.permutation(
                np.arange(1, flows[i-1] + 1)))

    def decodingStep(self, v, a, b, c, show=False):
        """
        Step of the decoding process.

        Args:
            v (array): Chromosome (K+J)
            a (array): Capacity of source k
            b (array): Demand on depot j
            c (matrix): transportation cost of one unit of product from
            source k to depot j.
        """
        cost, g, active = _decodingStep(v, a, b, c)
        return cost, g, active

    def decode(self, data):
        """
        Decode the chromosome into a solution.

        Returns:
        - Decision variables: X ... V.
        """

        # Pistachio factories -> pistachio consumers

        # Source capacity
        # amount coming from the processing center * factory production rate
        a1 = data.gammak * data.Cpw

        # Demand from each depot
        b1 = data.Dp

        # Total cost = transportation cost + production cost
        c1 = data.Cp + data.Cw[:, None]

        # Calculating cost and transportation matrix
        totalcost, self.P, self.A1 = self.decodingStep(self.S1, a1, b1, c1)

        # --------------------------------------------------------------------------------------------------------
        # Cosmetics factories -> cosmetics consumers
        a2 = data.gammas * data.Cpv
        b2 = data.Ds
        c2 = data.Cl + data.Cv[:, None]
        # L = how much cosmetic was sent to each consumer
        cost2, self.L, self.A2 = self.decodingStep(self.S2, a2, b2, c2)
        totalcost += cost2


        # --------------------------------------------------------------------------------------------------------
        # Oil extraction centers -> oil consumers + cosmetics factories
        # oil extraction center production capacity x (1 - oil loss percentage in the extraction process)
        a3 = (1 - data.lamb) * data.Cpr
        # oil consumers demand + amount of oil that should be sent to cosmetics factories (amount calculated in the previous flow / factory production rate)
        b3 = np.hstack((data.Du, np.sum(self.L, axis=1) / data.gammas))
        # transportation cost from oil extraction center to oil consumer + transportation cost from oil extraction center to cosmetics factory
        c3 = np.hstack(
            (data.CN + data.Cr[:, None], data.CS + data.Cr[:, None]))
        # OOc is an array with the amount of product that should be sent to each of the oil consumers and to the cosmetics factory (hence it needs to be split in two arrays)
        cost3, OOc, self.A3 = self.decodingStep(self.S3, a3, b3, c3)
        totalcost += cost3

        self.O = OOc[:, :data.N2]
        self.Oc = OOc[:, data.N2:]

        # --------------------------------------------------------------------------------------------------------
        # Processing center -> pistachio factories + oil extraction centers

        # Step 1: Processing center -> pistachio factories
        a4 = data.Cpu * (1 - data.beta) * data.theta[0]
        b4 = np.sum(self.P, axis=1) / data.gammak
        _, self.Go, self.A4 = self.decodingStep(self.S4, a4, b4, data.CK + data.Cu1[:, None])

        # --------------------------------
        # Step 2: Processing center -> oil extraction center
        a5 = data.Cpu * (1 - data.beta) * data.theta[1]
        b5 = (np.sum(self.O, axis=1) + np.sum(self.Oc, axis=1)) / (1 - data.lamb)
        _, self.Gr, self.A5 = self.decodingStep(self.S5, a5, b5, data.CE + data.Cu2[:, None])

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

            if self.Gr[j, :].sum() == 0 and self.Go[j, :].sum() == 0:
                continue

            # If the demand related to pistachio factories is higher
            if bX1[j] > bX2[j]:

                # The final processing center demand is the demand related to pistachio factories
                b[j] = bX1[j]

                # Calculate how much raw kernel should leave the processing center
                amount = b[j] * data.theta[1] * (1 - data.beta)

                # Find which oil extraction center has the lowest cost
                sorted_indices = np.argsort(data.CE[j, :] + data.Cu2[j])
                for e in sorted_indices:
                    if self.Gr[:, e].sum() + amount <= data.Cpr[e]:
                        break
                    # If all oil extraction centers have reached their capacity
                    elif self.Gr[:, e].sum() + amount > data.Cpr[e] and e == sorted_indices[-1]:
                        return float('inf')  # Infeasible solution

                # Assign to that segment the amount of raw kernel needed to complete the final demand
                self.Gr[j, e] = self.Gr[j, e] + amount - np.sum(self.Gr[j, :])

            # Otherwise
            elif bX1[j] < bX2[j]:
                # The final processing center demand is the demand related to the oil extraction center
                b[j] = bX2[j]

                # Calculate how much open-mouth pistachio should leave the processing center
                amount = b[j] * data.theta[0] * (1 - data.beta)

                sorted_indices = np.argsort(data.CK[j, :] + data.Cu1[j])
                for k in sorted_indices:
                    if self.Go[:, k].sum() + amount <= data.Cpw[k]:
                        break
                    # If all pistachio factories have reached their capacity
                    elif self.Go[:, k].sum() + amount > data.Cpw[k] and k == sorted_indices[-1]:
                        return float('inf')  # Infeasible solution

                # Assign to that segment the amount of open-mouth pistachio needed to complete the final demand
                self.Go[j, k] = self.Go[j, k] + amount - np.sum(self.Go[j, :])

        # Calculate cost
        totalcost += np.sum((data.CK + data.Cu1[:, None]) * self.Go) + np.sum(
            (data.CE + data.Cu2[:, None]) * self.Gr)

        # --------------------------------------------------------------------------------------------------------
        # Pistachio producers -> processing centers
        a6 = data.Cpa
        b6 = np.sum(self.Go, axis=1) / (1 - data.beta) / data.theta[0]
        c6 = data.CX + data.CI[:, None]
        cost6, self.X, self.A6 = self.decodingStep(self.S6, a6, b6, c6)
        totalcost += cost6

        # --------------------------------------------------------------------------------------------------------
        # Composting centers -> composting consumers
        a7 = data.gammaq * data.Cpy
        b7 = data.Dc
        c7 = data.Cd + data.Cy[:, None]
        cost7, self.D, self.A7 = self.decodingStep(self.S7, a7, b7, c7)
        totalcost += cost7

        # --------------------------------------------------------------------------------------------------------
        # Processing centers + oil extraction centers -> composting centers

        # Define the flow matrix between processing centers and composting centers
        self.Gw = np.zeros((data.J, data.Q))

        # The amount of waste to be sent by the processing centers
        a8 = np.sum(self.X, axis=0) * data.theta[2]

        # The minimum amount of waste needed by the composting centers
        b8 = np.sum(self.D, axis=1) / data.gammaq
        b8[b8 > data.Cpy] = data.Cpy[b8 > data.Cpy]  # Demand cannot exceed capacity

        # The amount of waste received in each composting center
        Cpy = np.zeros(data.Q)

        # For each processing center
        for j in range(data.J):
            # Identify the composting center with the lowest cost
            # and that has not yet reached its capacity
            sorted_indices = np.argsort(data.CJ[j, :])
            for q in sorted_indices:
                if Cpy[q] + a8[j] <= data.Cpy[q]:
                    break
                # If all composting centers have reached their capacity
                elif Cpy[q] >= data.Cpy[q] and q == sorted_indices[-1]:
                    return float('inf')  # Infeasible solution

            # Assign all the waste to that segment
            self.Gw[j, q] = a8[j]
            Cpy[q] += a8[j]

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
            a8 = np.sum(self.Gr, axis=0) * data.lamb

            # If the total available from sources is less than the total demand from depots
            if np.sum(a8) < np.sum(b8):

                # Scale down the demand to match the available supply
                delta = np.sum(b8)/np.sum(a8)
                b8 = b8 / delta
                # print(f"S8 = {self.S8}, a8={a8}, b8={b8}, data.CQ={data.CQ}")
                _, self.Ow, self.A8 = self.decodingStep(self.S8, a8, b8, data.CQ)
                
                # Composting centers -> composting consumers
                # Recalcular S7 devido a mudanças em Ow
                a7_new = data.gammaq * (np.sum(self.Gw, axis=0) + np.sum(self.Ow, axis=0))
                b7_new = data.Dc
                c7_new = data.Cd + data.Cy[:, None]
                totalcost -= cost7
                cost7_new, self.D, self.A7 = self.decodingStep(self.S7, a7_new, b7_new, c7_new)
                totalcost += cost7_new
            else:
                # Calculating cost and transportation matrix
                # print(f"S8 = {self.S8}, a8={a8}, b8={b8}, data.CQ={data.CQ}")
                _, self.Ow, self.A8 = self.decodingStep(self.S8, a8, b8, data.CQ)

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

    def encode(self, a, b, c, g):
        """
        Procedure of encoding a transportation tree.
        Args:
            a(array): capacity of source k
            b(array): demand on depot j
            c(matrix): transportation cost of one unit of product from source k to depot j
            g(matrix): amount of shipment from source k to depot j
        Returns:
            V(array): chromosome
        """
        pass

    def convert2sparse(self):
        """
        Convert the decision variables to a sparse matrix.
        """
        self.X = csr_matrix(self.X)
        self.Go = csr_matrix(self.Go)
        self.Gr = csr_matrix(self.Gr)
        self.Gw = csr_matrix(self.Gw)
        self.O = csr_matrix(self.O)
        self.Oc = csr_matrix(self.Oc)
        self.Ow = csr_matrix(self.Ow)
        self.L = csr_matrix(self.L)
        self.P = csr_matrix(self.P)
        self.D = csr_matrix(self.D)

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

        self.convert2sparse()
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
            (np.sum(self.X, axis=1).flatten(), data.Cpa.flatten(), "<=", "(1)"),
            (np.sum(self.X, axis=0).flatten(), data.Cpu.flatten(), "<=", "(2)"),
            ((np.sum(self.Gw, axis=0) + np.sum(self.Ow, axis=0)).flatten(), data.Cpy.flatten(), "<=", "(3)"),
            (np.sum(self.Go, axis=0).flatten(), data.Cpw.flatten(), "<=", "(4)"),
            (np.sum(self.Gr, axis=0).flatten(), data.Cpr.flatten(), "<=", "(5)"),
            (np.sum(self.Oc, axis=0).flatten(), data.Cpv.flatten(), "<=", "(6)"),
            (np.sum(self.Go, axis=1).flatten() + np.sum(self.Gr, axis=1).flatten() +
             np.sum(self.Gw, axis=1).flatten(), np.sum(self.X, axis=0).flatten(), "<=", "(7)"),
            (np.sum(self.Go, axis=1).flatten(), (1-data.beta) *
             data.theta[0]*np.sum(self.X, axis=0).flatten(), "==", "(8)"),
            (np.sum(self.Gr, axis=1).flatten(), (1-data.beta) *
             data.theta[1]*np.sum(self.X, axis=0).flatten(), "==", "(9)"),
            (np.sum(self.Gw, axis=1).flatten(),
             data.theta[2] * np.sum(self.X, axis=0).flatten(), "==", "(10)"),
            (np.sum(self.P, axis=1).flatten(), data.gammak *
             np.sum(self.Go, axis=0).flatten(), "<=", "(12)"),
            (np.sum(self.O, axis=1).flatten() + np.sum(self.Oc, axis=1).flatten(),
             (1-data.lamb) * np.sum(self.Gr, axis=0).flatten(), "<=", "(13)"),
            (np.sum(self.Ow, axis=1).flatten(), data.lamb *
             np.sum(self.Gr, axis=0).flatten(), "<=", "(14)"),
            (np.sum(self.L, axis=1).flatten(), data.gammas *
             np.sum(self.Oc, axis=0).flatten(), "<=", "(15)"),
            (np.sum(self.D, axis=1).flatten(), data.gammaq *
             (np.sum(self.Gw, axis=0).flatten() + np.sum(self.Ow, axis=0).flatten()), "<=", "(16)"),
            (np.sum(self.P, axis=0).flatten(), data.Dp.flatten(), ">=", "(17)"),
            (np.sum(self.O, axis=0).flatten(), data.Du.flatten(), ">=", "(18)"),
            (np.sum(self.L, axis=0).flatten(), data.Ds.flatten(), ">=", "(19)"),
            (np.sum(self.D, axis=0).flatten(), data.Dc.flatten(), "<=", "(20)")
        ]

        for lhs, rhs, comparison, label in equations:
            if comparison == "<=":
                result = np.all(lhs - rhs <= 1e-10)
            elif comparison == "==":
                result = np.all(np.abs(lhs - rhs) < 1e-10)
            elif comparison == ">=":
                result = np.all(lhs - rhs >= -1e-10)
            else:
                raise ValueError("Invalid comparison operator")

            if not result and (comparison == "=="):
                failed_restrictions.append(
                    f"Restriction {label} failed: {lhs} {comparison} {rhs}. Residual={np.abs(lhs-rhs)}")
            elif not result:
                failed_restrictions.append(
                    f"Restriction {label} failed: {lhs} {comparison} {rhs}")

        if not failed_restrictions:
            print("All restrictions have been respected.")
            return True, None
        else:
            print("The following restrictions have been violated:")
            for restriction in failed_restrictions:
                print(restriction)
            return False, failed_restrictions
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False
    
@jit(nopython=True, cache=True)
def _decodingStep(v, a, b, c):
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

if __name__ == "__main__":
    from Problem import loadInstance
    from time import time
    problem = loadInstance("data_100", quiet=True)
    solution = Solution()
    solution.generateChromosomeDeterministic(problem)
    totaltime = 0
    for i in range(10):
        tic = time()
        f = solution.evaluate(problem)
        toc = time()
        if i == 0:
            continue
        totaltime += toc - tic
    print(f"Total time: {totaltime} seconds")
    print(f"Objective function: {f}")
    