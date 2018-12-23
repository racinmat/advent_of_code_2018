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
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
