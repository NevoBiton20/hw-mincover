# import subprocess, sys
# subprocess.check_call([sys.executable, "-m", "pip", "install", "cvxpy"], stdout=subprocess.DEVNULL)
# subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx>=3.4"], stdout=subprocess.DEVNULL)

import networkx as nx, cvxpy, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
np.float_ = np.float64

def mincover(graph: nx.Graph) -> set:
    """
    Return a minimum-cardinality vertex cover in the given graph.
    
    >>> len(mincover(nx.Graph([(1,2),(2,3)])))
    1
    >>> len(mincover(nx.Graph([(1,2),(2,3),(3,1)])))
    2
    >>> len(mincover(nx.Graph([(1,2),(2,3),(3,4),(4,1)])))
    2
    >>> len(mincover(nx.Graph([])))
    0
    """

    nodes = list(graph.nodes)
    n = len(nodes)

    if graph.number_of_edges() == 0:
        return set()

    node_to_index = {
        node: i
        for i, node in enumerate(nodes)
    }

    # Objective: minimize x_1 + x_2 + ... + x_n
    c = np.ones(n)

    # Bounds: each variable is between 0 and 1
    bounds = Bounds(np.zeros(n), np.ones(n))

    # Integrality: each variable must be integer
    # Together with bounds [0, 1], this means each variable is binary.
    integrality = np.ones(n)

    # Constraints:
    # For every edge (u, v), require x_u + x_v >= 1
    A = []
    for u, v in graph.edges:
        row = np.zeros(n)
        row[node_to_index[u]] = 1
        row[node_to_index[v]] = 1
        A.append(row)

    A = np.array(A)

    constraints = LinearConstraint(
        A,
        lb=np.ones(len(A)),
        ub=np.full(len(A), np.inf)
    )

    result = milp(
        c=c,
        integrality=integrality,
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:
        raise RuntimeError("MILP solver failed: " + result.message)

    return {
        nodes[i]
        for i, value in enumerate(result.x)
        if value > 0.5
    }


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    # Use this code for testing via console input-output:
    edges=eval(input())
    graph = nx.Graph(edges)
    print(len(mincover(graph)))

