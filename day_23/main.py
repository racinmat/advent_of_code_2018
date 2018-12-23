import re
import numpy as np
import networkx as nx
from scipy import spatial


def load_input():
    points = []
    rs = []
    with open('input.txt', encoding='utf-8') as lines:
        for line in lines:
            m = re.match('pos=<(-?\d+),(-?\d+),(-?\d+)>, r=([- ]?\d+)', line)
            point = [int(i) for i in m.groups()[0:3]]
            r = int(m.groups()[3])
            points.append(point)
            rs.append(r)
    return np.array(points, dtype=np.int32), np.array(rs, dtype=np.int32)


# 7905 too low
def part_1():
    points, rs = load_input()
    max_point = points[np.argmax(rs)]
    dists = spatial.distance.cdist(max_point[np.newaxis, :], points, metric='cityblock')
    print(np.sum(dists <= np.max(rs)))


def part_2():
    points, rs = load_input()
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
    dense_dists = spatial.distance.pdist(points, metric='cityblock')
    distances = spatial.distance.squareform(dense_dists)
    sum_ranges = rs + rs[:, np.newaxis] - np.eye(rs.shape[0]) * rs * 2
    share_point = distances - sum_ranges
    share_point_dense = spatial.distance.squareform(share_point)

    print('dont share any point', np.sum(share_point_dense >= 0))
    print('share some points', np.sum(share_point_dense < 0))

    print()


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
