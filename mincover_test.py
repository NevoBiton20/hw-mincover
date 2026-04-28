import pytest
import networkx as nx
from mincover import mincover
from testcases import parse_testcases

testcases = parse_testcases("testcases.txt")

def run_testcase(input:str):
    graph = nx.Graph(input)
    cover = mincover(graph)
    return len(cover)

@pytest.mark.parametrize("testcase", testcases, ids=[testcase["name"] for testcase in testcases])
def test_cases(testcase):
    actual_output = run_testcase(testcase["input"])
    assert actual_output == testcase["output"], f"Expected {testcase['output']}, got {actual_output}"


def test_new_cases():
    def is_vertex_cover(graph: nx.Graph)->set:
        var = {node: cvxpy.Variable(boolean=True) for node in graph.nodes}
        objective = sum(var[node]
            for node in graph.nodes
        )   
        constraints = [
            var[u] + var[v] >= 1 for u,v in graph.edges
        ]
        prob = cvxpy.Problem(cvxpy.Minimize(objective), constraints)
        prob.solve(solver=cvxpy.SCIPY)
        return {node for node,nodevar in var.items() if nodevar.value>0}
    
    random_cases = [
        # name, number of vertices, edge probability, seed, expected min cover size
        ("small sparse random graph", 6, 0.3, 1, 3),
        ("small medium random graph", 8, 0.4, 2, 3),
        ("medium dense random graph", 10, 0.5, 3, 6),
        ("medium sparse random graph", 12, 0.25, 4, 5),

        # larger random graphs
        ("large sparse random graph", 20, 0.2, 5, 10),
        ("large medium random graph", 30, 0.3, 6, 21),
        ("very large dense random graph", 50, 0.5, 7, 43),
        ("very large very dense random graph", 50, 0.8, 8, 46),
        ("very large sparse random graph", 50, 0.2, 9, 37),
    ]

    for name, n, p, seed, expected_size in random_cases:
        graph = nx.gnp_random_graph(n, p, seed=seed)

        cover = mincover(graph)

        assert is_vertex_cover(graph, cover), f"{name}: returned set is not a vertex cover"
        assert len(cover) == expected_size, (
            f"{name}: expected size {expected_size}, got {len(cover)}"
        )
