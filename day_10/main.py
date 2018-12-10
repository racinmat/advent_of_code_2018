import re
import numpy as np
from PIL import Image


def load_points():
    points = []
    velocities = []
    with open('input.txt', encoding='utf-8') as lines:
        # position=<-10401, -42384> velocity=< 1,  4>
        for line in lines:
            m = re.match('position=<([- ]?\d+), ([- ]?\d+)> velocity=<([- ]?\d+), ([- ]?\d+)>', line)
            points.append([int(i) for i in m.groups()[0:2]])
            velocities.append([int(i) for i in m.groups()[2:4]])
    points = np.array(points)
    velocities = np.array(velocities)
    return points, velocities


def points_to_matrix(points):
    normed_points = points - points.min(axis=0)
    matrix = np.zeros((normed_points[:, 1].max() + 1, normed_points[:, 0].max() + 1), np.uint8)
    matrix[normed_points[:, 1], normed_points[:, 0]] = 1
    return matrix


def get_points_shape(points):
    return points[:, 1].max() - points[:, 1].min(), points[:, 0].max() - points[:, 0].min()


def part_1():
    points, velocities = load_points()
    curr_points = points.copy()
    matrix_sizes = []
    smallest_time = 0
    for i in range(100000):
        curr_points += velocities
        # don't need to build matrix to analyze its shape
        matrix_shape = get_points_shape(curr_points)
        matrix_sizes.append(matrix_shape)
        # print(matrix_shape)
        if i > 2 and (matrix_sizes[-1][0] > matrix_sizes[-2][0] or matrix_sizes[-1][1] > matrix_sizes[-2][1]):
            print('previous was local minimum')
            print(matrix_shape)
            smallest_time = i
            break

    print(smallest_time)
    # analyzing shapes
    for i in range(smallest_time - 10, smallest_time + 10):
        curr_points = points + i * velocities
        matrix = points_to_matrix(curr_points)

        # text printing, good only for small matrices
        # string_matrix = np.chararray(matrix.shape)
        # string_matrix[:] = '.'
        # string_matrix[matrix == 1] = '#'
        # [print(''.join(i)) for i in string_matrix.decode('utf-8')]
        # print()

        # saving as image
        Image.fromarray((1 - matrix) * 255).save('im-{}.png'.format(i))


def part_2():
    points, velocities = load_points()
    curr_points = points.copy()
    matrix_sizes = []
    smallest_time = 0
    for i in range(100000):
        curr_points += velocities
        # don't need to build matrix to analyze its shape
        matrix_shape = get_points_shape(curr_points)
        matrix_sizes.append(matrix_shape)
        # print(matrix_shape)
        if i > 2 and (matrix_sizes[-1][0] > matrix_sizes[-2][0] or matrix_sizes[-1][1] > matrix_sizes[-2][1]):
            print('previous was local minimum')
            print(matrix_shape)
            smallest_time = i
            break

    print(smallest_time)


if __name__ == '__main__':
    part_1()
    part_2()
