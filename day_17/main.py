import re
from itertools import product

import numpy as np
from PIL import Image
from scipy import signal

CLAY = 3
FREE = 5
WATER = 7
PUDDLE = 11  # louže, stojatá voda
# using lowest non-1 primes to guarrante unique results of convolutions

# for better visual control
m = {
    '|': WATER,
    '#': CLAY,
    '.': FREE,
    '~': PUDDLE,
}


def load_input():
    clays = []
    with open('input.txt', encoding='utf-8') as lines:
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
    # everything is in bowl-like shape, so puddle spread should be working, can match corner patterns
    # todo: implement puddle to know which water is stackable upwards
    # todo: find number which will be unique indentifiers for 4 classes on 2x2 metrics
    conditions = [
        ['|',  # ['|',
         '.'],  # '|'],
        ['.|',  # ['||',
         '##'],  # '##'],
        ['|.',  # ['||',
         '##'],  # '##'],
        ['#|',  # ['#~',
         '##'],  # '##'],
        ['|#',  # ['~#',
         '##'],  # '##'],
        ['~|'],  # ['~~'],
        ['|~'],  # ['~~'],
        ['.|',  # ['||',
         '~~'],  # '~~'],
        ['|.',  # ['||',
         '~~'],  # '~~'],
        ['#||',
         '#~~'],
        ['||#',
         '~~#'],
        ['#|#',
         '#~#'],
    ]
    results = [
        ['|',
         '|'],
        ['||',
         '##'],
        ['||',
         '##'],
        ['#~',
         '##'],
        ['~#',
         '##'],
        ['~~'],
        ['~~'],
        ['||',
         '~~'],
        ['||',
         '~~'],
        ['#~~',
         '#~~'],
        ['~~#',
         '~~#'],
        ['#~#',
         '#~#'],
    ]
    conditions = [[[m[char] for char in row] for row in c] for c in conditions]
    results = [[[m[char] for char in row] for row in c] for c in results]
    conv_conditions = [np.flip(np.flip(np.array(c), 0), 1) for c in conditions]  # need to flip for convolution
    conv_conditions = [1 / c for c in conv_conditions]  # so multiplication results in 1 in match case
    results = [np.array(res) for res in results]
    return conditions, results, conv_conditions


def get_right_border(grid, y, x):
    curr_x = x
    while True:
        if curr_x >= grid.shape[1]:
            return None
        if np.isin(grid[y + 1, curr_x], [FREE, WATER]):
            return None
        if grid[y, curr_x + 1] == CLAY:
            break
        curr_x += 1
    return curr_x


def get_left_border(grid, y, x):
    curr_x = x
    while True:
        if curr_x < 0:
            return None
        if np.isin(grid[y + 1, curr_x], [FREE, WATER]):
            return None
        if grid[y, curr_x - 1] == CLAY:
            break
        curr_x -= 1
    return curr_x


def tick(grid, conditions, results, conv_conditions):
    # apparently convolution is nice for water falling down, but apparently cant solve everything and thus I will go to graph-style solution
    # matches = []
    # for condition, result in zip(conv_conditions, results):
    #     res = signal.convolve2d(grid, condition) == condition.size
    #     indices = np.where(res)
    #     if len(indices[0]) > 0:
    #         for y, x in zip(*indices):
    #             matches.append(((y, x), result))
    #
    # # apply only lowest level of changes should not be needed
    # # max_y = max([indices[0] for indices, result in matches])
    # # matches = [(indices, result) for indices, result in matches if indices[0] == max_y]
    #
    # for indices, result in matches:
    #     y, x = indices
    #     # todo: check 2x1 matrix indices
    #     y_from, y_to = y - round(result.shape[0] / 2), y - round(result.shape[0] / 2) + result.shape[0]
    #     x_from, x_to = x - round(result.shape[1] / 2), x - round(result.shape[1] / 2) + result.shape[1]
    #     grid[y_from:y_to, x_from:x_to] = result
    # return grid

    # water falling down
    water_to_fall = np.where((grid == WATER) & (np.roll(grid, -1, axis=0) == FREE))
    for y, x in zip(*water_to_fall):
        floors = y + np.where(grid[y:, x] == CLAY)[0]
        if len(floors) == 0:
            # hit the bottom
            grid[y:, x] = WATER
        else:
            first_clay_y = min(floors)
            grid[y:first_clay_y, x] = WATER

    # steady water/puddle spreading to sides
    puddle_to_spread = np.where((grid == WATER) & (np.isin(np.roll(grid, -1, axis=0), [CLAY, PUDDLE])))
    for y, x in zip(*puddle_to_spread):
        right_border = get_right_border(grid, y, x)
        left_border = get_left_border(grid, y, x)
        if right_border is None or left_border is None:
            continue  # nowhere to spread, hole somewhere
        # todo: add border check and other rules
        first_clay_right_x = right_border
        first_clay_left_x = left_border
        grid[y, first_clay_left_x:first_clay_right_x+1] = PUDDLE

    # falling water spreading to sides
    water_to_spread = np.where((grid == WATER) & (np.isin(np.roll(grid, -1, axis=0), [CLAY, PUDDLE])))
    # add some checker to stop evaluating what has already been evaluated
    for y, x in zip(*water_to_spread):
        right_border = get_right_border(grid, y, x)
        left_border = get_left_border(grid, y, x)
        if right_border is not None and left_border is not None:
            continue  # earlier case, should spread puddle

        right_stream_down = np.where((grid[y, x:] == WATER) & (np.isin(grid[y + 1, x:], [WATER])))[0]
        left_stream_down = np.where((grid[y, :x] == WATER) & (np.isin(grid[y + 1, :x], [WATER])))[0]
        # this finds streams from different water, I must check proximity, probably?
        # todo: detect only nearest stream down, probably manually, not by numpy
        if len(right_stream_down) > 0 or len(left_stream_down) > 0:
            continue  # already evaluated stream

        right_hole = np.where((grid[y, x:] == FREE) & (np.isin(grid[y + 1, x:], [FREE])))[0]
        left_hole = np.where((grid[y, :x] == FREE) & (np.isin(grid[y + 1, :x], [FREE])))[0]
        # todo: add border check and other rules
        first_clay_right_x = grid.shape[1]
        if len(right_hole) > 0:
            first_clay_right_x = min(first_clay_right_x, x + min((right_hole + 1).tolist()))  # exclusive to inclusive
        if right_border is not None:
            first_clay_right_x = min(right_border + 1, first_clay_right_x)

        first_clay_left_x = 0
        if len(left_hole) > 0:
            first_clay_left_x = max(first_clay_left_x, max(left_hole.tolist()))
        if left_border is not None:
            first_clay_left_x = max(left_border, first_clay_left_x)
        grid[y, first_clay_left_x:first_clay_right_x] = WATER

    # working filling part of first bowl
    return grid


def show_conv_collisions():
    conditions, results, conv_conditions = prepare_rules()
    rules_shapes = set([c.shape for c in conv_conditions])
    # splitting by shape
    rules_by_shapes = dict()
    for shape in rules_shapes:
        rules_by_shapes[shape] = [i for i, c in enumerate(conv_conditions) if c.shape == shape]

    for shape, indices in rules_by_shapes.items():
        for i in indices:
            conv_condition, result, condition = conv_conditions[i], results[i], np.array(conditions[i])
            matches = 0
            matched = []
            all_combinations = list(product(m.values(), repeat=condition.size))
            for variant in all_combinations:
                grid_part = np.array(variant).reshape(shape)

                res = signal.convolve2d(grid_part, conv_condition) == condition.size
                indices = np.where(res)
                if len(indices[0]) > 0:
                    matches += len(indices[0])
                    matched.append(grid_part)

            print('found ', matches, ' matches for one condition')


def print_grid(grid):
    string_grid = np.where(grid == FREE, '.', '?')
    string_grid[grid == WATER] = '|'
    string_grid[grid == PUDDLE] = '~'
    string_grid[grid == CLAY] = '#'

    [print(''.join(i)) for i in string_grid]
    print()


def part_1():
    # show_conv_collisions()
    # return
    old_grid = prepare_data()
    old_grid = old_grid[:800, :]
    conditions, results, conv_conditions = prepare_rules()
    i = 0
    while True:
        new_grid = tick(old_grid.copy(), conditions, results, conv_conditions)
        # print_grid(new_grid)
        grid_to_save = new_grid[:800, :]
        Image.fromarray(((grid_to_save / grid_to_save.max()) * 255).astype(np.uint8)).save('im-{}.png'.format(i))
        if np.allclose(old_grid, new_grid):
            break
        old_grid = new_grid
        i += 1
    print(np.sum(np.isin(new_grid, [WATER, PUDDLE])) - 1)  # - 1 for spring


def part_2():
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
