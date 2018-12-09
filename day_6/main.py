from scipy import spatial
import numpy as np


def dist(p_1, p_2):
    return abs(p_1[0] - p_2[0]) + abs(p_1[1] - p_2[1])


def nearest_point(p):
    dist_dict = {suspect: dist(suspect, p) for suspect in suspects_list}
    return min(dist_dict, key=dist_dict.get)



def part_1():
    suspects_list = []
    suspects_dict = dict()
    with open('input.txt', encoding='utf-8') as lines:
        for idx, line in enumerate(lines):
            point = tuple([int(i) for i in line.replace('\n', '').split(', ')])
            suspects_list.append(point)
            suspects_dict[point] = idx

    suspects = np.array(suspects_list)

    rect = np.ones((suspects[:, 0].max(), suspects[:, 1].max())) * -1

    # frontier suspects are nearest neighbours of all border points and thus have infinity neighbours
    border_points = []
    border_points += [(i, 0) for i in range(rect.shape[0])]
    border_points += [(i, rect.shape[1] - 1) for i in range(rect.shape[0])]
    border_points += [(0, i) for i in range(rect.shape[1])]
    border_points += [(rect.shape[0] - 1, i) for i in range(rect.shape[1])]

    frontier_suspects = set([nearest_point(point) for point in border_points])

    enclosed_suspects = set(suspects_list) - frontier_suspects

    kd_tree = spatial.cKDTree(suspects_list)
    indices = np.indices(rect.shape).reshape((2, -1))
    distances, suspect_indices = kd_tree.query(indices.T, k=2, p=1, distance_upper_bound=max(rect.shape) * 2)
    min_suspect_indices = suspect_indices[:, 0]
    min_suspect_indices[distances[:, 0] - distances[:, 1] == 0] = -1
    rect[indices[0], indices[1]] = min_suspect_indices

    frontier_indices = [suspects_dict[i] for i in enclosed_suspects]
    sums = [np.sum(rect == idx) for idx in frontier_indices]
    max_count = max(sums)

    print(max_count)


def part_2():
    suspects_list = []
    with open('../day_6_part_1/input.txt', encoding='utf-8') as lines:
        for idx, line in enumerate(lines):
            point = tuple([int(i) for i in line.replace('\n', '').split(', ')])
            suspects_list.append(point)

    suspects = np.array(suspects_list)

    rect = np.ones((suspects[:, 0].max(), suspects[:, 1].max())) * -1

    # frontier suspects are nearest neighbours of all border points and thus have infinity neighbours

    kd_tree = spatial.cKDTree(suspects_list)
    indices = np.indices(rect.shape).reshape((2, -1))
    distances, suspect_indices = kd_tree.query(indices.T, k=len(suspects_list), p=1,
                                               distance_upper_bound=max(rect.shape) * 2)
    print((distances.sum(axis=1) < 10000).sum())


if __name__ == '__main__':
    part_1()
    part_2()
