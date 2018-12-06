from scipy import spatial
import numpy as np

if __name__ == '__main__':
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
                                               distance_upper_bound=max(rect.shape)*2)
    print((distances.sum(axis=1) < 10000).sum())
