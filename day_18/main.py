import numpy as np
from scipy import signal, ndimage

# 2, 7 and 137 are distinguishable from each other for convolution on range 0-8
TREE = 2
LUMBER = 17
OPEN = 0

MIDDLE = 137


def load_data():
    lines_array = []
    with open('input.txt', encoding='utf-8') as lines:
        for line in lines:
            lines_array.append(list(line.replace('\n', '')))
    string_map = np.array(lines_array)
    grid = np.ones_like(string_map, dtype=np.int32) * 0
    grid[string_map == '#'] = LUMBER
    grid[string_map == '.'] = OPEN
    grid[string_map == '|'] = TREE
    return grid


def apply_rules_for_generation_conv(grid):
    new_gen_grid = grid.copy()
    # new_gen_grid = np.zeros_like(grid)
    # new_gen_grid[grid == LUMBER] = LUMBER   # lumber is set now and replaced later

    # 1) open with 3 or more trees around -> tree
    # 2) tree with 3 or more lumbers -> lumber
    # 3) lumber with no tree and no lumber around -> open

    rule = np.array([
        [1, 1, 1],
        [1, MIDDLE, 1],
        [1, 1, 1],
    ])
    # todo: add options to all others (any number of trees for lumbers check, any number of lumbers for tree check...)
    # rules are symmetric and thus flip invariant, no need for flipping
    # conv_res = signal.convolve2d(grid, rule, mode='same')
    conv_res = ndimage.convolve(grid, rule, mode='constant')
    #
    # conv_res = signal.fftconvolve(grid, rule, mode='same')

    middle_pos, around = np.divmod(conv_res, MIDDLE)
    around_lumbers, around_trees = np.divmod(around, LUMBER)
    around_trees = np.round(around_trees / TREE).astype(np.int32)
    # 1)
    # big magic with coprimes and modulo, muhaha
    should_appear_tree = (middle_pos == OPEN) & (around_trees >= 3)
    indices = np.where(should_appear_tree)
    new_gen_grid[indices] = TREE

    # 2)
    should_appear_lumber = (middle_pos == TREE) & (around_lumbers >= 3)
    indices = np.where(should_appear_lumber)
    new_gen_grid[indices] = LUMBER

    # 3)
    should_appear_open = (middle_pos == LUMBER) & ((around_lumbers < 1) | (around_trees < 1))
    indices = np.where(should_appear_open)
    new_gen_grid[indices] = OPEN

    return new_gen_grid


def calc_next_generation(grid):
    new_gen_grid = apply_rules_for_generation_conv(grid)
    return new_gen_grid


def calc_generation_sum(i):
    if i < 100:
        raise RuntimeError("Please, run the usual way")
    else:
        # computed from first 100 iterations by hand, during the first 100 it has constant growth
        return 186 * (i - 100) + 19623


def print_grid(grid):
    string_grid = np.where(grid == TREE, '|', '?')
    string_grid[grid == LUMBER] = '#'
    string_grid[grid == OPEN] = '.'

    [print(''.join(i)) for i in string_grid]
    print()


def find_smallest_usable_coprimes():
    # feasibles = []
    # options = np.arange(1, 9, 1)
    # for i in range(1, 20):
    #     for j in range(i, 20):
    #         # if len(set(options * i).intersection(set(options * j))) <= 1:
    #         #     print(i, j, 'feasible coprimes')
    #         #     feasibles.append([i, j])
    #         if max(options * i) < min(options * j):
    #             print(i, j, 'feasible coprimes')
    #             feasibles.append([i, j])
    # feasibles = np.array(feasibles)
    # diffs = np.abs(feasibles[:, 0] - feasibles[:, 1])
    # print(feasibles)
    # print(diffs)

    feasibles = []
    options = np.arange(1, 9, 1)
    for i in range(1, 200):
        for j in range(i, 200):
            for k in range(j, 200):
                if max(options * i) < min(options * j) and max(options * j) < min(options * k):
                    print(i, j, k, 'feasible coprimes')
                    feasibles.append([i, j, k])
    feasibles = np.array(feasibles)
    diffs = np.abs(feasibles[:, 0] - feasibles[:, 1])
    print(feasibles)
    print(diffs)


def generate_values(grid):
    values = []
    # print_grid(grid)
    values.append(np.sum(grid == TREE) * np.sum(grid == LUMBER))
    for i in range(0, 8000):
        grid = calc_next_generation(grid)
        value = np.sum(grid == TREE) * np.sum(grid == LUMBER)
        values.append(value)

    return values


def calc_value(iteration, grid):
    x_offset = 1000

    if iteration < x_offset:
        # print_grid(grid)
        for i in range(0, iteration):
            grid = calc_next_generation(grid)
            # print_grid(grid)
        return np.sum(grid == TREE) * np.sum(grid == LUMBER)

    period = 28
    series = [174420, 179800, 182590, 189630, 196452, 205000, 210789, 218240, 222824, 231336, 236155, 240482, 237636,
              237082, 234938, 237900, 232232, 228274, 220584, 216752, 206702, 199824, 178100, 175587, 169880, 173014,
              171248, 174782]
    value = series[(iteration - x_offset) % period]
    return value


def part_1():
    # find_smallest_usable_coprimes()

    grid = load_data()
    value = calc_value(10, grid)
    print(value)


# 179800 too high
def part_2():
    # consistency check
    grid = load_data()
    all_values = generate_values(grid.copy())
    values = all_values[700:]
    modeled_values = [calc_value(i, grid.copy()) for i in range(700, 8000)]
    print(np.allclose(values, modeled_values))

    # print(calc_value(1000000000))

    # values = generate_values()

    # import matplotlib.pyplot as plt
    # plt.plot(np.arange(0, len(values), 1), values)
    # # plt.plot(np.arange(0, len(values) - 1, 1), np.diff(diff_sums))
    # plt.show()
    print()


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
