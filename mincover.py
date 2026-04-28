# import subprocess, sys
# subprocess.check_call([sys.executable, "-m", "pip", "install", "cvxpy"], stdout=subprocess.DEVNULL)
# subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx>=3.4"], stdout=subprocess.DEVNULL)

import networkx as nx, cvxpy, numpy as np
np.float_ = np.float64

def mincover(graph: nx.Graph)->set:
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
    # I chose to implement this function using the branch-and-bound algorithm
    graph = graph.copy()
    best = set(graph.nodes)

    def search(G, cover):
        nonlocal best

        # If current cover is already not better, stop
        if len(cover) >= len(best):
            return

        # If no edges remain, we found a valid cover
        if G.number_of_edges() == 0:
            best = set(cover)
            return

        matching = nx.maximal_matching(G)
        if len(cover) + len(matching) >= len(best):
            return

        # Pick an edge
        u, v = next(iter(G.edges))

        # include u
        G1 = G.copy()
        G1.remove_node(u)
        search(G1, cover | {u})

        # include v
        G2 = G.copy()
        G2.remove_node(v)
        search(G2, cover | {v})

    search(graph, set())
    return best


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    # Use this code for testing via console input-output:
    edges=eval(input())
    graph = nx.Graph(edges)
    print(len(mincover(graph)))

