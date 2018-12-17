import re
import numpy as np
from scipy import signal

CLAY = -1
FREE = 1
WATER = 2


def load_input():
    clays = []
    with open('test_input.txt', encoding='utf-8') as lines:
        for line in lines:
            m = re.match('([xy])=(\d+)\.?\.?(\d+)?, ([xy])=(\d+)\.?\.?(\d+)?', line.replace('\n', ''))
            g = m.groups()
            coord_1 = g[0]
            range_1 = int(g[1]) if g[2] is None else range(int(g[1]),
                                                           int(g[2]) + 1)  # from inclusive to exclusive range
            coord_2 = g[3]
            range_2 = int(g[4]) if g[5] is None else range(int(g[4]),
                                                           int(g[5]) + 1)  # from inclusive to exclusive range
            data = {
                coord_1: range_1,
                coord_2: range_2,
            }
            clays.append(data)
    return clays


def prepare_data():
    clays = load_input()
    # normalize clays x
    x_min = min([min(c['x']) if isinstance(c['x'], range) else c['x'] for c in clays])
    for c in clays:
        if isinstance(c['x'], range):
            c['x'] = range(c['x'].start - x_min, c['x'].stop - x_min)
        else:
            c['x'] -= x_min

    x_max = max([max(c['x']) if isinstance(c['x'], range) else c['x'] for c in clays])
    y_max = max([max(c['y']) if isinstance(c['y'], range) else c['y'] for c in clays])

    grid = np.ones((y_max + 1, x_max + 1)) * FREE
    for c in clays:
        grid[c['y'], c['x']] = CLAY

    grid[0, 500 - x_min] = WATER
    return grid


def prepare_rules():
    conditions = [
        [[WATER],
         [FREE]],
        [[FREE, WATER],
         [CLAY, CLAY]],
        [[WATER, FREE],
         [CLAY, CLAY]],
        [[WATER, FREE],
         [WATER, WATER]],
        [[FREE, WATER],
         [WATER, WATER]],
        [[FREE, WATER],
         [CLAY, WATER]],
        [[WATER, FREE],
         [WATER, CLAY]],
        [[WATER, FREE],
         [CLAY, FREE]],
        [[FREE, WATER],
         [FREE, CLAY]],
    ]
    results = [
        [[WATER],
         [WATER]],
        [[WATER, WATER],
         [CLAY, CLAY]],
        [[WATER, WATER],
         [CLAY, CLAY]],
        [[WATER, WATER],
         [WATER, WATER]],
        [[WATER, WATER],
         [WATER, WATER]],
        [[WATER, WATER],
         [CLAY, WATER]],
        [[WATER, WATER],
         [WATER, CLAY]],
        [[WATER, WATER],
         [CLAY, FREE]],
        [[WATER, WATER],
         [FREE, CLAY]],
    ]
    conv_conditions = [np.flip(np.flip(np.array(c), 0), 1) for c in conditions]  # need to flip for convolution
    results = [np.array(res) for res in results]
    return conditions, results, conv_conditions


def tick(grid, conditions, results, conv_conditions):
    matches = []
    for condition, result in zip(conv_conditions, results):
        res = signal.convolve2d(grid, condition) == (condition ** 2).sum()
        indices = np.where(res)
        if len(indices[0]) > 0:
            for y, x in zip(*indices):
                matches.append(((y, x), result))

    # apply only lowest level of changes:
    max_y = max([indices[0] for indices, result in matches])
    matches = [(indices, result) for indices, result in matches if indices[0] == max_y]

    for indices, result in matches:
        y, x = indices
        y_from, y_to = y - round(result.shape[0] / 2), y - round(result.shape[0] / 2) + result.shape[0]
        x_from, x_to = x - round(result.shape[1] / 2), x - round(result.shape[1] / 2) + result.shape[1]
        grid[y_from:y_to, x_from:x_to] = result
    return grid


def print_grid(grid):
    string_grid = np.where(grid == FREE, '.', '#')
    string_grid[grid == WATER] = '|'

    [print(''.join(i)) for i in string_grid]
    print()


def part_1():
    old_grid = prepare_data()
    conditions, results, conv_conditions = prepare_rules()
    while True:
        new_grid = tick(old_grid.copy(), conditions, results, conv_conditions)
        print_grid(new_grid)
        if np.allclose(old_grid, new_grid):
            break
        old_grid = new_grid
    print(np.sum(new_grid == WATER))


def part_2():
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
