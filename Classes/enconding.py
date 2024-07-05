import random


class Encoding:
    def __init__(self, g, c, a, b):
        self.g = g
        self.c = c
        self.a = a
        self.b = b

    def leafNodes(self):
        """
        Procedure for finding the cheapest node among the leaf nodes.
        """
        leaf_nodes = []
        num_sources = len(self.a)
        num_depots = len(self.b)

        # For each source and depot, check if it is a leaf node
        for source_index in range(num_sources):
            # Calculate total outgoing shipment from this source
            outgoing_shipment = sum(self.g[source_index])
            # If the outgoing shipment equals the capacity of the source
            if outgoing_shipment == self.a[source_index]:
                connected_depots = [i for i in range(
                    # Find connected depots
                    num_depots) if self.g[source_index][i] > 0]
                if len(connected_depots) == 1:  # If there's only one connected depot
                    depot_index = connected_depots[0]
                    # Amount transported to the depot
                    transported_amount = self.g[source_index][depot_index]
                    # Cost of transportation
                    transportation_cost = self.c[source_index][depot_index]
                    total_cost = transported_amount * transportation_cost  # Total cost
                    leaf_nodes.append(
                        (source_index, depot_index, total_cost, 'source'))

        # For each depot, check if it is a leaf node
        for depot_index in range(num_depots):
            # Calculate total incoming shipment to this depot
            incoming_shipment = sum(self.g[i][depot_index]
                                    for i in range(num_sources))
            # If the incoming shipment equals the demand of the depot
            if incoming_shipment == self.b[depot_index]:
                connected_sources = [i for i in range(
                    # Find connected sources
                    num_sources) if self.g[i][depot_index] > 0]
                if len(connected_sources) == 1:  # If there's only one connected source
                    source_index = connected_sources[0]
                    # Amount transported from the source
                    transported_amount = self.g[source_index][depot_index]
                    # Cost of transportation
                    transportation_cost = self.c[source_index][depot_index]
                    total_cost = transported_amount * transportation_cost  # Total cost
                    leaf_nodes.append(
                        (source_index, depot_index, total_cost, 'depot'))

        leaf_nodes.sort(key=lambda x: x[2])  # Sort based on total cost
        return leaf_nodes

    def generateChromosome(self):
        num_nodes = len(self.a) + len(self.b)
        assigned_numbers = [0] * num_nodes

        leaf_nodes = self.leafNodes()

        # Assign unique numbers to each leaf node based on their cost
        for idx, (source, depot, total_cost, node_type) in enumerate(leaf_nodes):
            if node_type == 'source':
                assigned_numbers[source] = num_nodes - idx
            elif node_type == 'depot':
                assigned_numbers[depot + len(self.a)] = num_nodes - idx

        # Find the smallest number not assigned
        smallest_number = min(num for num in assigned_numbers if num > 0)

        # Assign numbers to the remaining nodes
        remaining_nodes = [i for i, num in enumerate(
            assigned_numbers) if num == 0]
        remaining_numbers = list(range(smallest_number - 1, 0, -1))
        random.shuffle(remaining_numbers)

        for node_idx in remaining_nodes:
            assigned_numbers[node_idx] = remaining_numbers.pop()

        return assigned_numbers


# Example usage:
g = [[300, 0, 250, 0], [0, 300, 0, 0], [0, 50, 50, 350]]
c = [[11, 19, 17, 18], [16, 14, 18, 15], [15, 16, 19, 13]]
a = [550, 300, 450]
b = [300, 350, 300, 350]

encoding = Encoding(g, c, a, b)
leaf_nodes = encoding.leafNodes()
print(leaf_nodes)

chromosome = encoding.generateChromosome()
print("Encoded chromosome:", chromosome)
