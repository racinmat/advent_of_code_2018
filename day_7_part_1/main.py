from scipy import spatial
import numpy as np


def get_roots():
    return np.logical_and(adjacency.sum(axis=0) == 0, adjacency.sum(axis=1) > 0)


if __name__ == '__main__':
    from time import time
    start = time()
    edges = []
    nodes = set()

    with open('input.txt', encoding='utf-8') as lines:
        for line in lines:
            node_from, node_to = line[5], line[36]
            edges.append((node_from, node_to))
            nodes.add(node_from)
            nodes.add(node_to)

    nodes = list(sorted(nodes))
    nodes_np = np.array(nodes)
    nodes_idx = {v: k for k, v in enumerate(nodes)}

    adjacency = np.zeros((len(nodes), len(nodes)))
    for node_from, node_to in edges:
        adjacency[nodes_idx[node_from], nodes_idx[node_to]] = 1

    topological_order = []

    # must use DFS because of alphabetical ordering
    while len(topological_order) < len(nodes):
        roots = get_roots()
        root_nodes = sorted(nodes_np[roots])
        if not root_nodes:  # adding leaves when no other nodes remain
            root_nodes = list(set(nodes) - set(topological_order))
        root = root_nodes[0]
        root_idx = nodes_idx[root]
        adjacency[root_idx, :] = 0
        topological_order.append(root)

    print(''.join(topological_order))
    print(time() - start)
