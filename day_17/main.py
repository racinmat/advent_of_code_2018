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
    # -1 to have 1 free column for overflow
    x_min = min([min(c['x']) if isinstance(c['x'], range) else c['x'] for c in clays]) - 1
    y_min = min([min(c['y']) if isinstance(c['y'], range) else c['y'] for c in clays]) - 1
    for c in clays:
        if isinstance(c['x'], range):
            c['x'] = range(c['x'].start - x_min, c['x'].stop - x_min)
        else:
            c['x'] -= x_min
        if isinstance(c['y'], range):
            c['y'] = range(c['y'].start - y_min, c['y'].stop - y_min)
        else:
            c['y'] -= y_min

    x_max = max([max(c['x']) if isinstance(c['x'], range) else c['x'] for c in clays])
    y_max = max([max(c['y']) if isinstance(c['y'], range) else c['y'] for c in clays])

    grid = np.ones((y_max + 1, x_max + 2)) * FREE   # to have 1 padding on right side
    for c in clays:
        grid[c['y'], c['x']] = CLAY

    grid[0, 500 - x_min] = WATER
    return grid


def get_right_border(grid, y, x, cache):
    if (y, x) in cache['right_border']:
        right_border = cache['right_border'][(y, x)]
        # check cached solution and check if stream is still here
        if np.all(np.isin(grid[y + 1, x:right_border], [CLAY, PUDDLE])) and grid[y, right_border + 1] == CLAY:
            return right_border

    curr_x = x
    while True:
        if curr_x >= grid.shape[1]:
            return None
        if np.isin(grid[y + 1, curr_x], [FREE, WATER]):
            return None
        if grid[y, curr_x + 1] == CLAY:
            break
        curr_x += 1
    cache['right_border'][(y, x)] = curr_x
    return curr_x


def get_left_border(grid, y, x, cache):
    if (y, x) in cache['left_border']:
        left_border = cache['left_border'][(y, x)]
        # check cached solution and check if stream is still here
        if np.all(np.isin(grid[y + 1, left_border:x], [CLAY, PUDDLE])) and grid[y, left_border - 1] == CLAY:
            return left_border

    curr_x = x
    while True:
        if curr_x < 0:
            return None
        if np.isin(grid[y + 1, curr_x], [FREE, WATER]):
            return None
        if grid[y, curr_x - 1] == CLAY:
            break
        curr_x -= 1
    cache['left_border'][(y, x)] = curr_x
    return curr_x


def get_right_stream_down(grid, y, x, cache):
    if (y, x) in cache['right_stream_down']:
        left_stream_down = cache['right_stream_down'][(y, x)]
        # check cached solution and check if stream is still here
        if grid[y, left_stream_down] == WATER and grid[y + 1, left_stream_down] == WATER:
            return left_stream_down

    curr_x = x
    while True:
        if curr_x >= grid.shape[1]:
            return None
        if grid[y, curr_x] == WATER and grid[y + 1, curr_x] == WATER:
            break
        # is water spread in same iteration and did not go down yet
        if grid[y, curr_x] == WATER and grid[y + 1, curr_x] == FREE:
            break
        if np.isin(grid[y + 1, curr_x], [FREE, WATER]) or np.isin(grid[y, curr_x], [CLAY, PUDDLE]):
            return None
        curr_x += 1
    cache['right_stream_down'][(y, x)] = curr_x
    return curr_x


def get_left_stream_down(grid, y, x, cache):
    if (y, x) in cache['left_stream_down']:
        left_stream_down = cache['left_stream_down'][(y, x)]
        # check cached solution and check if stream is still here
        if grid[y, left_stream_down] == WATER and grid[y + 1, left_stream_down] == WATER:
            return left_stream_down

    curr_x = x
    while True:
        if curr_x < 0:
            return None
        if grid[y, curr_x] == WATER and grid[y + 1, curr_x] == WATER:
            break
        # is water spread in same iteration and did not go down yet
        if grid[y, curr_x] == WATER and grid[y + 1, curr_x] == FREE:
            break
        if np.isin(grid[y + 1, curr_x], [FREE, WATER]) or np.isin(grid[y, curr_x], [CLAY, PUDDLE]):
            return None
        curr_x -= 1
    cache['left_stream_down'][(y, x)] = curr_x
    return curr_x


def tick(grid, cache):
    # water falling down
    water_to_fall = np.where((grid == WATER) & (np.roll(grid, -1, axis=0) == FREE))
    for y, x in zip(*water_to_fall):
        floors = y + np.where(np.isin(grid[y:, x], [CLAY, PUDDLE]))[0]
        if len(floors) == 0:
            # hit the bottom
            grid[y:, x] = WATER
        else:
            first_clay_y = min(floors)
            grid[y:first_clay_y, x] = WATER

    # steady water/puddle spreading to sides: water, clay or puddle below it, free or clay next to it on both sides
    puddle_to_spread = np.where((grid == WATER) &
                                (np.isin(np.roll(grid, -1, axis=0), [CLAY, PUDDLE])) &
                                ((np.isin(np.roll(grid, 1, axis=1), [CLAY, FREE])) |
                                 (np.isin(np.roll(grid, -1, axis=1), [CLAY, FREE]))))
    for y, x in zip(*puddle_to_spread):
        if (y, x) in cache['puddle_to_spread']:
            continue

        right_border = get_right_border(grid, y, x, cache)
        left_border = get_left_border(grid, y, x, cache)
        if right_border is None or left_border is None:
            continue  # nowhere to spread, hole somewhere

        first_clay_right_x = right_border
        first_clay_left_x = left_border
        grid[y, first_clay_left_x:first_clay_right_x + 1] = PUDDLE
        cache['puddle_to_spread'].add((y, x))

    # falling water spreading to sides: water, puddle or clay below it, and free left or right from it
    water_to_spread = np.where((grid == WATER) &
                               (np.isin(np.roll(grid, -1, axis=0), [CLAY, PUDDLE])) &
                               ((np.isin(np.roll(grid, 1, axis=1), [FREE])) |
                                (np.isin(np.roll(grid, -1, axis=1), [FREE]))))
    # add some checker to stop evaluating what has already been evaluated
    for y, x in zip(*water_to_spread):
        if (y, x) in cache['water_to_spread']:
            continue

        right_border = get_right_border(grid, y, x, cache)
        left_border = get_left_border(grid, y, x, cache)
        if right_border is not None and left_border is not None:
            continue  # earlier case, should spread puddle

        right_stream_down = get_right_stream_down(grid, y, x, cache)
        left_stream_down = get_left_stream_down(grid, y, x, cache)

        # to be more robust, will solve left and right separately
        if right_stream_down is None:
            # creating right stream down
            right_hole = np.where((grid[y, x:] == FREE) & (np.isin(grid[y + 1, x:], [FREE])))[0]
            first_clay_right_x = grid.shape[1]
            if len(right_hole) > 0:
                first_clay_right_x = min(first_clay_right_x, x + min((right_hole + 1).tolist()))  # exclusive to inclusive
            if right_border is not None:
                first_clay_right_x = min(right_border + 1, first_clay_right_x)
            grid[y, x:first_clay_right_x] = WATER

        if left_stream_down is None:
            # creating left stream down
            left_hole = np.where((grid[y, :x] == FREE) & (np.isin(grid[y + 1, :x], [FREE])))[0]
            first_clay_left_x = 0
            if len(left_hole) > 0:
                first_clay_left_x = max(first_clay_left_x, max(left_hole.tolist()))
            if left_border is not None:
                first_clay_left_x = max(left_border, first_clay_left_x)
            grid[y, first_clay_left_x:x] = WATER

        cache['water_to_spread'].add((y, x))

    # working filling part of first bowl
    return grid, cache


def print_grid(grid):
    string_grid = np.where(grid == FREE, '.', '?')
    string_grid[grid == WATER] = '|'
    string_grid[grid == PUDDLE] = '~'
    string_grid[grid == CLAY] = '#'

    [print(''.join(i)) for i in string_grid]
    print()


def part_1():
    old_grid = prepare_data()
    old_grid = old_grid[:, :]
    i = 0

    cache = {'water_to_spread': set(), 'puddle_to_spread': set(), 'left_stream_down': dict(),
             'right_stream_down': dict(), 'left_border': dict(), 'right_border': dict()}

    while True:
        new_grid, cache = tick(old_grid.copy(), cache)
        # print_grid(new_grid)
        grid_to_save = new_grid
        Image.fromarray(((grid_to_save / grid_to_save.max()) * 255).astype(np.uint8)).save('im-{}.png'.format(i))
        if np.allclose(old_grid, new_grid):
            break
        old_grid = new_grid
        i += 1
    print(np.sum(np.isin(new_grid, [WATER, PUDDLE])) - 1)  # - 1 for spring


def part_2():
    old_grid = prepare_data()
    old_grid = old_grid[:, :]
    i = 0

    cache = {'water_to_spread': set(), 'puddle_to_spread': set(), 'left_stream_down': dict(),
             'right_stream_down': dict(), 'left_border': dict(), 'right_border': dict()}

    while True:
        new_grid, cache = tick(old_grid.copy(), cache)
        # print_grid(new_grid)
        grid_to_save = new_grid
        Image.fromarray(((grid_to_save / grid_to_save.max()) * 255).astype(np.uint8)).save('im-{}.png'.format(i))
        if np.allclose(old_grid, new_grid):
            break
        old_grid = new_grid
        i += 1
    print(np.sum(np.isin(new_grid, [PUDDLE])))


if __name__ == '__main__':
    from time import time

    start = time()

    # part_1()
    part_2()

    print(time() - start)
