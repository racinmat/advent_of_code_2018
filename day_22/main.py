import re
import numpy as np
import networkx as nx

ROCKY = 0
WET = 1
NARROW = 2

NEITHER = 0
TORCH = 1
GEAR = 2


def load_input():
    with open('input.txt', encoding='utf-8') as lines:
        depth_line = next(lines)
        target_line = next(lines)
    m = re.match('depth: (\d+)', depth_line)
    depth = int(m.group(1))
    m = re.match('target: (\d+),(\d+)', target_line)
    target = int(m.group(2)), int(m.group(1))  # to load into y, x numpy format
    return depth, target


def geo_to_erosion(geo, depth):
    return (geo + depth) % 20183


def build_grid(depth, target, size):
    geo_idx = np.zeros(size, dtype=np.int32)
    geo_idx[0, 0] = 0
    geo_idx[target] = 0
    geo_idx[:, 0] = np.arange(0, geo_idx.shape[0]) * 48271
    geo_idx[0, :] = np.arange(0, geo_idx.shape[1]) * 16807
    for i in range(1, geo_idx.shape[0]):
        for j in range(1, geo_idx.shape[1]):
            if (i, j) == target:
                continue
            geo_idx[i, j] = geo_to_erosion(geo_idx[i - 1, j], depth) * geo_to_erosion(geo_idx[i, j - 1], depth)
    # row_part = (geo_to_erosion(geo_idx[1:, 0], depth) ** np.arange(1, geo_idx.shape[0]))
    # column_part = (geo_to_erosion(geo_idx[0, 1:], depth) ** np.arange(1, geo_idx.shape[1]))
    # geo_idx[1:, 1:] = row_part * column_part[:, np.newaxis]

    erosion = geo_to_erosion(geo_idx, depth)
    cave_type = erosion % 3

    for i in range(1, geo_idx.shape[0]):
        for j in range(1, geo_idx.shape[1]):
            if (i, j) == target:
                continue
            assert geo_idx[i, j] == erosion[i - 1, j] * erosion[i, j - 1]

    return geo_idx, erosion, cave_type


def print_grid(cave_type):
    string_grid = np.chararray(cave_type.shape, unicode=True)
    string_grid[cave_type == ROCKY] = '.'
    string_grid[cave_type == WET] = '='
    string_grid[cave_type == NARROW] = '|'

    string_grid[0, 0] = 'M'
    string_grid[-1, -1] = 'T'
    [print(''.join(i)) for i in string_grid]
    print()


# 7905 too low
def part_1():
    depth, target = load_input()

    geo_idx, erosion, cave_type = build_grid(depth, target, (target[0] + 1, target[1] + 1))
    # print_grid(cave_type)
    print(np.sum(cave_type))


def part_2():
    depth, target = load_input()

    geo_idx, erosion, cave_type = build_grid(depth, target, (target[0] + 200, target[1] + 200))
    equipment = [NEITHER, TORCH, GEAR]
    allowed_equipment = {
        ROCKY: {GEAR, TORCH},
        WET: {GEAR, NEITHER},
        NARROW: {TORCH, NEITHER}}
    g = nx.Graph()

    for i, j in np.ndindex(geo_idx.shape):
        for k in equipment:
            g.add_node((i, j, k))

    for i, j in np.ndindex(geo_idx.shape):
        allowed_from = allowed_equipment[cave_type[i, j]]
        for k in allowed_from:
            for i2, j2 in [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]:
                if i2 < 0 or j2 < 0 or i2 >= geo_idx.shape[0] or j2 >= geo_idx.shape[1]:
                    continue
                allowed_to = allowed_equipment[cave_type[i2, j2]]
                if k not in allowed_to:
                    continue
                g.add_edge((i, j, k), (i2, j2, k), weight=1)
            for k2 in allowed_from - {k}:
                g.add_edge((i, j, k), (i, j, k2), weight=7)

    # path = nx.dijkstra_path(g, (0, 0, TORCH), (target[0], target[1], TORCH))
    # print(path)
    path_length = nx.dijkstra_path_length(g, (0, 0, TORCH), (target[0], target[1], TORCH))
    print(path_length)


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
