import numpy as np
from scipy import signal, ndimage

# 2 and 9 are distinguishable from each other for convolution on range 0-8
TREE = 2
LUMBER = 9
OPEN = 0


def load_data():
    lines_array = []
    with open('test_input.txt', encoding='utf-8') as lines:
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
    # 1) open with 3 or more trees around -> tree
    # 2) tree with 3 or more lumbers -> lumber
    # 3) lumber with no tree and no lumber around -> open

    rule = np.array([
        [1, 1, 1],
        [1, 100, 1],
        [1, 1, 1],
    ])
    conv_res = signal.convolve2d(grid, rule, mode='valid')

    # 1)
    matches = np.array([TREE * 3, TREE * 4, TREE * 5, TREE * 6, TREE * 7, TREE * 8])
    # rules are symmetric and thus flip invariant, no need for flipping
    indices = np.where(np.isin(conv_res, matches))
    new_gen_grid[indices] = TREE

    # 2)
    matches = np.array([LUMBER * 3, LUMBER * 4, LUMBER * 5, LUMBER * 6, LUMBER * 7, LUMBER * 8]) + LUMBER * 100
    indices = np.where(np.isin(conv_res, matches))
    new_gen_grid[indices] = LUMBER

    # 3)
    matches = np.array([100, 100 + LUMBER, 100 + TREE])
    indices = np.where(np.isin(conv_res, matches))
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
    feasibles = []
    options = np.arange(0, 9, 1)
    for i in range(1, 20):
        for j in range(i, 20):
            if len(set(options * i).intersection(set(options * j))) <= 1:
                print(i, j, 'feasible coprimes')
                feasibles.append([i, j])
    feasibles = np.array(feasibles)
    diffs = np.abs(feasibles[:, 0] - feasibles[:, 1])
    print(feasibles)
    print(diffs)


def part_1():
    # find_smallest_usable_coprimes()

    grid = load_data()
    for i in range(0, 10):
        grid = calc_next_generation(grid)
        print_grid(grid)
    print(np.sum(grid == TREE) * np.sum(grid == LUMBER))


def part_2():
    print(calc_generation_sum(50000000000))
    # print(calc_generation_sum(200))
    # diff_sums = get_diff_sums()
    # import matplotlib.pyplot as plt
    # # plt.plot(np.arange(0, len(diff_sums), 1), diff_sums)
    # plt.plot(np.arange(0, len(diff_sums) - 1, 1), np.diff(diff_sums))
    # plt.show()
    # print(np.bincount(diff_sums))
    # plants_indices = np.where(plants == 1)[0] + total_offset
    # total_sum = np.sum(plants_indices)
    # print(total_sum)


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
