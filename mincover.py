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
    nodes = list(graph.nodes)

    def generate_subsets_of_size(k, start, current):
        """
        Recursively generate all subsets of size k.
        """
        if len(current) == k:
            yield set(current)
            return

        for i in range(start, len(nodes)):
            current.append(nodes[i])
            yield from generate_subsets_of_size(k, i + 1, current)
            current.pop()

    for k in range(len(nodes) + 1):
        for cover in generate_subsets_of_size(k, 0, []):
            if all(u in cover or v in cover for u, v in graph.edges):
                return cover


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    # Use this code for testing via console input-output:
    edges=eval(input())
    graph = nx.Graph(edges)
    print(len(mincover(graph)))

