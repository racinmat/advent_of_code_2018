import numpy as np


def get_roots(adjacency):
    return np.logical_and(adjacency.sum(axis=0) == 0, adjacency.sum(axis=1) > 0)


def load_graph():
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
    return edges, nodes, nodes_idx, nodes_np


def task_time(node):
    return ord(node) - 4
    # return ord(node) - 64


def show_graph_with_labels(adjacency_matrix, mylabels):
    rows, cols = np.where(adjacency_matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())
    import networkx as nx
    import matplotlib.pyplot as plt
    gr = nx.DiGraph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=500, labels=mylabels, with_labels=True, arrows=True)
    plt.show()


def get_root_nodes(adjacency, nodes, nodes_np, topological_order):
    roots = get_roots(adjacency)
    root_nodes = sorted(nodes_np[roots])
    if not root_nodes:  # adding leaves when no other nodes remain
        root_nodes = list(set(nodes) - set(topological_order))
    return root_nodes


def remove_root(adjacency, nodes_idx, root, topological_order):
    root_idx = nodes_idx[root]
    adjacency[root_idx, :] = 0
    topological_order.append(root)


def part_1():
    edges, nodes, nodes_idx, nodes_np = load_graph()
    adjacency = build_adjacency_matrix(edges, nodes, nodes_idx)

    topological_order = []

    # must use DFS because of alphabetical ordering
    while len(topological_order) < len(nodes):
        root_nodes = get_root_nodes(adjacency, nodes, nodes_np, topological_order)
        root = root_nodes[0]
        remove_root(adjacency, nodes_idx, root, topological_order)

    print(''.join(topological_order))


def part_2():
    # from time import time

    # start = time()
    edges, nodes, nodes_idx, nodes_np = load_graph()
    adjacency = build_adjacency_matrix(edges, nodes, nodes_idx)

    # show_graph_with_labels(adjacency, {k: v for k, v in enumerate(nodes)})
    topological_order = []

    # must use DFS because of alphabetical ordering
    second = 0
    workers_num = 5
    workers_remaining = np.zeros((workers_num))
    workers_task = [None] * workers_num
    # print('Second  W0  W1  W2  W3  W4   Open  Done')

    while len(topological_order) < len(nodes):
        root_nodes = get_root_nodes(adjacency, nodes, nodes_np, topological_order)
        root_nodes = sorted(set(root_nodes) - set(workers_task))  # skipping WIP

        for i in range(workers_num):
            if not root_nodes:
                break
            # assigning job to worker
            if workers_task[i] is not None:
                continue
            task = root_nodes.pop(0)
            workers_remaining[i] = task_time(task)
            workers_task[i] = task
            # all tasks allocated

        jump = max(1, int(workers_remaining[workers_remaining > 0].min()))  # fast forward some iterations

        for i in range(workers_num):
            workers_remaining[i] -= jump  # tick
            # check the done job
            if workers_remaining[i] > 0:
                continue
            done_task = workers_task[i]
            if done_task is not None:
                remove_root(adjacency, nodes_idx, done_task, topological_order)
                workers_task[i] = None

        second += jump

    print(second)
    # print(time() - start)


def build_adjacency_matrix(edges, nodes, nodes_idx):
    adjacency = np.zeros((len(nodes), len(nodes)))
    for node_from, node_to in edges:
        adjacency[nodes_idx[node_from], nodes_idx[node_to]] = 1
    return adjacency


if __name__ == '__main__':
    part_1()
    part_2()
