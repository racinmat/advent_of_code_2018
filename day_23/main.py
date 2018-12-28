import re
import numpy as np
import networkx as nx
from scipy import spatial
import z3


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


def part_1():
    points, rs = load_input()
    max_point = points[np.argmax(rs)]
    dists = spatial.distance.cdist(max_point[np.newaxis, :], points, metric='cityblock')
    print(np.sum(dists <= np.max(rs)))


def part_2():
    points, rs = load_input()

    # just some playing with z3
    # a = z3.Real('a')
    # b = z3.Real('b')
    # s = z3.Solver()
    # s.add(a + b == 5)
    # s.add(a - 2*b == 3)
    # s.add(a - 2*b == 3)
    # check_result = s.check()
    # m = s.model()
    # print(m[a])
    # print(m[b])

    # a = z3.Real('a')
    # b = z3.Real('b')
    # c = z3.Real('c')
    # d = z3.Real('d')
    # s = z3.Optimize()
    # s.add()
    # s.add(a <= 5)
    # s.add(b <= 10)
    # s.add(b >= c)
    # s.add(a >= d)
    # obj = s.maximize(a + b + c + d)
    # while s.check() == z3.sat:
    #     m = s.model()
    #     print(m[a])
    #     print(m[b])
    #     print(m[c])
    #     print(m[d])
    #     print(obj.value())
    # check_res = s.check()
    # m = s.model()
    # print(m[a])
    # print(m[b])
    # print(m[c])
    # print(m[d])
    # print(obj.value())

    # x, y = z3.Ints('x y')
    # opt = z3.Optimize()
    # opt.set(priority='pareto')
    # opt.add(x + y == 10, x >= 0, y >= 0)
    # mx = opt.maximize(x)
    # my = opt.maximize(y)
    # while opt.check() == z3.sat:
    #     print(mx.value(), my.value())
    # pass
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
    def z3abs(x):
        # z3.fpAbs is not working on integers, somehow, this works
        return z3.If(x >= 0, x, -x)

    coords = z3.Ints('x y z')
    s = z3.Optimize()
    in_ranges = z3.Ints(' '.join('p'+str(i) for i in range(len(points))))
    for i, (point, r) in enumerate(zip(points, rs)):
        # coords_diff = [z3abs(j - int(k)) for j, k in zip(coords, point)]  # casting from numpy type to pure python
        coords_diff = [z3abs(j - int(k)) for j, k in zip(coords, point)]  # casting from numpy type to pure python
        manhattan_dist = z3.Sum(coords_diff)
        s.add(z3.If(manhattan_dist <= int(r), 1, 0) == in_ranges[i])
    dist_from_zero = z3.Int('dist')
    # s.add(dist_from_zero == z3.Sum([z3abs(i) for i in coords]))
    s.add(dist_from_zero == z3.Sum([z3abs(i) for i in coords]))
    s.maximize(z3.Sum(in_ranges))
    s.minimize(dist_from_zero)
    res = s.check()
    m = s.model()
    print([m[i] for i in coords], m[dist_from_zero])


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
