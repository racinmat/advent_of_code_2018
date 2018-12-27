import re
import numpy as np
import networkx as nx
from scipy import spatial


def load_input():
    points = []
    with open('input.txt', encoding='utf-8') as lines:
        for line in lines:
            point = [int(i) for i in line.split(',')]
            points.append(point)
    return np.array(points, dtype=np.int32)


# 571 too high
def part_1():
    points = load_input()
    dense_dists = spatial.distance.pdist(points, metric='cityblock')
    distances = spatial.distance.squareform(dense_dists)
    clusters = np.arange(0, distances.shape[0], 1)
    neighbours_from, neighbours_to = np.where((distances != 0) & (distances <= 3))
    edges = np.stack((clusters[neighbours_from[neighbours_from < neighbours_to]],
                      clusters[neighbours_to[neighbours_from < neighbours_to]]))

    # looks like a good union-find algorithm on undirected graph
    while edges.shape[1] > 0:
        parent, child = edges[:, 0]
        edges[edges == clusters[child]] = clusters[parent]
        clusters[clusters == clusters[child]] = clusters[parent]
        edges = edges[:, edges[0, :] != edges[1, :]]
        # merging one edge per iteration
    print(len(np.unique(clusters)))


def part_2():
    points = load_input()
    # reaches = np.zeros((np.max(points[:, 0]), np.max(points[:, 1]), np.max(points[:, 2])))
    # grid_indices = np.array(list(np.ndindex(reaches.shape)))
    # for point, r in zip(points, rs):
    #     dists = spatial.distance.cdist(point[np.newaxis, :], grid_indices, metric='cityblock')
    #     reach = np.where(dists <= r)
    #     reached_points = grid_indices[reach[1], :][:, 0], grid_indices[reach[1], :][:, 1], grid_indices[reach[1], :][:, 2]
    #     reaches[reached_points] += 1
    #
    # best_point = np.unravel_index(np.argmax(reaches), reaches.shape)
    # distance = spatial.distance.cityblock([0, 0, 0], best_point)
    # for point, r in zip(points, rs):
    #     range_set = set()
    #     for p0 in range(point[0] - r, point[0] + r + 1):
    #         remain_dist = r - abs(p0 - point[0])
    #         for p1 in range(point[1] - remain_dist, point[1] + remain_dist + 1):
    #             remain_dist = r - (abs(p0 - point[0]) + abs(p1 - point[1]))
    #             for p2 in range(point[2] - remain_dist, point[2] + remain_dist + 1):
    #                 range_set.add((p0, p1, p2))
    #     points_in_range.append(range_set)

    # dense_dists = spatial.distance.pdist(points, metric='cityblock')
    # distances = spatial.distance.squareform(dense_dists)
    # sum_ranges = rs + rs[:, np.newaxis] - np.eye(rs.shape[0]) * rs * 2
    # share_point = distances - sum_ranges
    # share_point_dense = spatial.distance.squareform(share_point)
    #
    # print('dont share any point', np.sum(share_point_dense >= 0))
    # print('share some points', np.sum(share_point_dense < 0))

    # mean for prunning estimate
    # centroid = np.mean(points, axis=0).astype(np.int32)
    # in_range = spatial.distance.cdist(centroid[np.newaxis, :], points, metric='cityblock') <= rs
    # np.sum(in_range)
    print()


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
