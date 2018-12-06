import sys
from scipy import spatial
import numpy as np


def dist(p_1, p_2):
    return abs(p_1[0] - p_2[0]) + abs(p_1[1] - p_2[1])


def nearest_point(p):
    min_suspect = None
    min_dist = sys.maxsize
    for suspect in suspects_list:
        distance = dist(suspect, p)
        if distance < min_dist:
            min_suspect = suspect
            min_dist = distance
    return min_suspect


if __name__ == '__main__':
    from time import time
    start = time()
    suspects_list = []
    suspects_dict = dict()
    with open('input.txt', encoding='utf-8') as lines:
        for idx, line in enumerate(lines):
            point = tuple([int(i) for i in line.replace('\n', '').split(', ')])
            suspects_list.append(point)
            suspects_dict[point] = idx

    suspects = np.array(suspects_list)

    print(time() - start)

    rect = np.zeros((suspects[:, 0].max(), suspects[:, 1].max()))
    rect_2 = np.zeros((suspects[:, 0].max(), suspects[:, 1].max()))

    # frontier suspects are nearest neighbours of all border points and thus have infinity neighbours
    frontier_suspects = set()
    border_points = []
    border_points += [(i, 0) for i in range(rect.shape[0])]
    border_points += [(i, rect.shape[1] - 1) for i in range(rect.shape[0])]
    border_points += [(0, i) for i in range(rect.shape[1])]
    border_points += [(rect.shape[0] - 1, i) for i in range(rect.shape[1])]

    for point in border_points:
        frontier_suspects.add(nearest_point(point))

    print(time() - start)

    enclosed_suspects = set(suspects_list) - frontier_suspects

    for x in range(rect.shape[0]):
        for y in range(rect.shape[1]):
            rect[x, y] = suspects_dict[nearest_point((x, y))]

    print(time() - start, 'usual')

    # kd_tree = spatial.KDTree(suspects_list)
    # indices = np.indices(rect_2.shape).reshape((2, -1))
    # _, min_suspect_indices = kd_tree.query(indices.T, p=1, distance_upper_bound=max(rect.shape))
    # rect_2[indices[0], indices[1]] = min_suspect_indices
    # print(time() - start, 'kd tree')

    print(np.allclose(rect, rect_2))

    frontier_indices = [suspects_dict[i] for i in enclosed_suspects]
    max_idx = None
    max_count = 0
    for idx in frontier_indices:
        count = np.sum(rect == idx)
        if count > max_count:
            max_idx = idx
            max_count = count

    print(max_count)
    print(time() - start)
