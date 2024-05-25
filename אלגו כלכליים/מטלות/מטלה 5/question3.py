import networkx as nx
import math
from typing import Union, List


def is_pareto_efficient(valuations: list[list[float]], allocations: list[list[float]])->bool:
    """
    Check if the given allocation is Pareto efficient by examining cycles in a directed graph.
    using the statements we proved in lecture 5 (belman ford , multiplication of weights <1 -> additions of logarithms of weights <0)

    >>> is_pareto_efficient([[50,1], [1, 100]], [[0,1], [1,0]])   
    False
    >>> is_pareto_efficient([[50,1], [1, 100]], [[1,0], [0,1]])
    True
    >>> is_pareto_efficient([[10, 20, 30, 40], [40, 30, 20, 10]], [[1, 1, 1, 1], [0, 0, 0, 0]]) # dictator 
    True
    >>> is_pareto_efficient([[10, 20, 30, 40], [40, 30, 20, 10]], [[0, 0.6, 1, 0.9], [1, 0.4, 0, 0.1]])
    False
    >>> is_pareto_efficient([[10, 20, 30, 40], [40, 30, 20, 10]], [[1, 0.7, 1, 0], [0, 0.3, 0, 0]])
    False
    """
    edges = []  # This will store the edges for our graph
    num_players = len(valuations)  # Number of players
    num_items = len(valuations[0])  # Number of items

    # Create edges for the graph
    for i in range(num_players):
        for j in range(num_players):
            if i != j:  # Ensure not creating a self-loop
                indices = [k for k in range(num_items) if allocations[i][k] != 0]  # Items allocated to player i
                if indices:
                    # Compute the minimum log ratio of valuations
                    min_ratio_log = min(math.log(valuations[i][k] / valuations[j][k]) for k in indices)
                    edges.append((i, j, min_ratio_log))  # Add edge to the list

    # Create a directed graph and add weighted edges
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    
    # Check for negative weight cycles in the graph
    return not nx.negative_edge_cycle(G)

def check_and_improve_pareto_effiecient(valuations: list[list[float]], allocations: list[list[float]])-> Union[bool, List]:
    """
    Improve the given allocation to make it Pareto efficient in case its not.
    same like Lecturer explained in class to switch fractions of the bundle along the cycle to improve the allocation

    >>> check_and_improve_pareto_effiecient([[10, 20, 30, 40], [40, 30, 20, 10]], [[1, 0.7, 1, 0], [0, 0.3, 0, 0]])
    [[0.996, 0.7001666666666666, 1, 0], [0.004, 0.29983333333333334, 0, 0]]
    >>> check_and_improve_pareto_effiecient([[10, 20, 30, 40], [40, 30, 20, 10], [40, 30, 20, 10]], [[1, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    [[0.996, 1, 0, 0.001], [0.004, 0, 0, 0.999], [0, 0, 1, 0]]
    >>> check_and_improve_pareto_effiecient([[20, 20, 20, 40], [40, 40, 10, 10]], [[1, 0.3, 0.9, 0], [0, 0.7, 0.1, 0]])
    [[0.998, 0.3, 0.901, 0], [0.002, 0.7, 0.099, 0]]
    >>> check_and_improve_pareto_effiecient([[10, 20, 30, 40], [40, 30, 20, 10]], [[1, 0.7, 1, 0], [0, 0.3, 0, 0]])
    [[0.996, 0.7001666666666666, 1, 0], [0.004, 0.29983333333333334, 0, 0]]
    >>> check_and_improve_pareto_effiecient([[10, 20, 30, 40], [40, 30, 20, 10], [40, 30, 20, 10]], [[1, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    [[0.996, 1, 0, 0.001], [0.004, 0, 0, 0.999], [0, 0, 1, 0]]
    >>> check_and_improve_pareto_effiecient([[20, 10, 30, 40], [30, 20, 10, 40]], [[1, 0.8, 1, 0], [0, 0.2, 0, 1]])
    [[1, 0.798, 1, 0.0005], [0, 0.202, 0, 0.9995]]
    >>> check_and_improve_pareto_effiecient([[25, 15, 35, 25], [15, 25, 25, 35]], [[1, 0.6, 0.4, 1], [0, 0.4, 0.6, 0]])
    [[1, 0.5983333333333333, 0.40084000000000003, 1], [0, 0.40166666666666667, 0.59916, 0]]
    >>> check_and_improve_pareto_effiecient([[35, 25, 20, 30], [20, 30, 35, 25]], [[0.9, 0.5, 1, 0.3], [0.1, 0.5, 0, 0.7]])
    [[0.901, 0.5, 0.99825, 0.3], [0.099, 0.5, 0.0017500000000000003, 0.7]]
    >>> check_and_improve_pareto_effiecient([[30, 20, 40, 10], [40, 30, 10, 20]], [[1, 1, 0, 0.5], [0, 0, 1, 0.5]])
    [[1, 1, 0.002, 0.498], [0, 0, 0.998, 0.502]]
    """
    edges = []  # This will store the edges for our graph
    item_dict = {}  # Dictionary to store items associated with each edge
    num_players = len(valuations)  # Number of players
    num_items = len(valuations[0])  # Number of items

    # Create edges for the graph
    for i in range(num_players):
        for j in range(num_players):
            if i != j:  # Ensure not creating a self-loop
                indices = [k for k in range(num_items) if allocations[i][k] != 0]  # Items allocated to player i
                if indices:
                    # Compute the minimum log ratio of valuations
                    min_ratio_log = min(math.log(valuations[i][k] / valuations[j][k]) for k in indices)
                    edges.append((i, j, min_ratio_log))  # Add edge to the list
                    item = min(indices, key=lambda k: math.log(valuations[i][k] / valuations[j][k]))
                    item_dict[(i, j)] = item  # Store the item associated with this edge

    # Create a directed graph and add weighted edges
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)

    try:
        # Try to find a negative weight cycle
        cycle = nx.find_negative_cycle(G, edges[0][0])
    except nx.NetworkXNoCycle:
        return True  # No cycle found means allocation is Pareto efficient

    epsilon = 0.001  # Small value for adjusting allocations
    for i in range(len(cycle) - 1):
        u, v = cycle[i], cycle[i + 1]
        item = item_dict[(u, v)]  # Get the item associated with the edge
        # Adjust allocations along the cycle
        allocations[v][item] += epsilon * valuations[v][item] / valuations[u][item]
        allocations[u][item] -= epsilon * valuations[v][item] / valuations[u][item]
        epsilon *= valuations[u][item] / valuations[v][item]  # Update epsilon based on the ratio

    return allocations  # Return the improved allocations

if __name__ == '__main__':
    import doctest
    doctest.testmod()
