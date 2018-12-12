import numpy as np
from scipy.signal import fftconvolve

def load_plants():
    with open('input.txt', encoding='utf-8') as lines:
        initial = next(lines)[15:].replace('\n', '').replace('#', '1').replace('.', '0')
        initial = list(initial)
        initial = np.array(list(map(int, initial)))
        next(lines)
        rules = dict()
        for line in lines:
            line = line.replace('\n', '').replace('#', '1').replace('.', '0')
            rule = list(map(int, line[:5]))
            result = int(line[9:])
            # skipping rules with 0
            if result == 0:
                continue
            rules[tuple(rule)] = result
    return initial, rules


# def apply_rules_for_generation(plants, rules):
#     new_gen_plants = np.zeros_like(plants)
#
#     for i in range(2, len(plants) - 2):
#         part = tuple(plants[i - 2:i + 3])
#         if part in rules:
#             new_gen_plants[i] = rules[part]
#     return new_gen_plants


def apply_rules_for_generation_conv(plants, rules, rules_results):
    new_gen_plants = np.ones_like(plants) * -1
    for i, rule in enumerate(rules):
        indices = np.where(np.convolve(plants, rule[::-1], mode='valid') == len(rule))[0]
        # indices = np.where(np.round(fftconvolve(plants, rule[::-1], mode='valid')) == len(rule))[0]
        indices += 2    # to align indices to the middle of array
        new_gen_plants[indices] = rules_results[i]
    return new_gen_plants


def calc_next_generation(plants, rules, rules_np, rules_results):
    plants = np.pad(plants, 4, 'constant', constant_values=-1)
    # new_gen_plants = apply_rules_for_generation(plants, rules)
    new_gen_plants = apply_rules_for_generation_conv(plants, rules_np, rules_results)
    # assert np.allclose(new_gen_plants, new_gen_plants_conv)
    plants_indices = np.where(new_gen_plants == 1)[0]
    plants_start = plants_indices.min()
    plants_end = plants_indices.max()
    return new_gen_plants[plants_start: plants_end + 1], plants_start - 4


def part_1():
    initial, rules = load_plants()
    plants = initial
    plants[plants == 0] = -1
    rules_np = np.array(list(rules.keys()))
    rules_np[rules_np == 0] = -1
    rules_results = list(rules.values())
    # print(''.join(map(str, plants)))
    total_offset = 0
    for i in range(0, 10000):
        plants, offset = calc_next_generation(plants, rules, rules_np, rules_results)
        total_offset += offset
        # print(''.join(map(str, plants)))
    plants_indices = np.where(plants == 1)[0] + total_offset
    total_sum = np.sum(plants_indices)
    print(total_sum)


# 187023 is correct answer after 1000 iterations

def part_2():
    initial, rules = load_plants()
    plants = initial
    rules_np = np.array(list(rules.keys()))
    rules_results = list(rules.values())
    # print(''.join(map(str, plants)))
    total_offset = 0
    for i in range(0, 50000000000):
        if i % 1000000 == 0:
            print('iter', i)
        plants, offset = calc_next_generation(plants, rules, rules_np, rules_results)
        total_offset += offset
        # print(''.join(map(str, plants)))
    plants_indices = np.where(plants == 1)[0] + total_offset
    total_sum = np.sum(plants_indices)
    print(total_sum)


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    # part_2()

    print(time() - start)

'''
#..#.#..##......###...###
#...#....#.....#..#..#..#
##..##...##....#..#..#..##
#.#...#..#.#....#..#..#...#
#.#..#...#.#...#..#..##..##
#...##...#.#..#..#...#...#
##.#.#....#...#..##..##..##
#..###.#...##..#...#...#...#
#....##.#.#.#..##..##..##..##
##..#..#####....#...#...#...#
#.#..#...#.##....##..##..##..##
#...##...#.#...#.#...#...#...#
##.#.#....#.#...#.#..##..##..##
#..###.#....#.#...#....#...#...#
#....##.#....#.#..##...##..##..##
##..#..#.#....#....#..#.#...#...#
#.#..#...#.#...##...#...#.#..##..##
#...##...#.#.#.#...##...#....#...#
##.#.#....#####.#.#.#...##...##..##
#..###.#..#.#.#######.#.#.#..#.#...#
#....##....#####...#######....#.#..##

#....##....#####...#######....#.#..##

...#..#.#..##......###...###...........
...#...#....#.....#..#..#..#...........
...##..##...##....#..#..#..##..........
..#.#...#..#.#....#..#..#...#..........
...#.#..#...#.#...#..#..##..##.........
....#...##...#.#..#..#...#...#.........
....##.#.#....#...#..##..##..##........
...#..###.#...##..#...#...#...#........
...#....##.#.#.#..##..##..##..##.......
...##..#..#####....#...#...#...#.......
..#.#..#...#.##....##..##..##..##......
...#...##...#.#...#.#...#...#...#......
...##.#.#....#.#...#.#..##..##..##.....
..#..###.#....#.#...#....#...#...#.....
..#....##.#....#.#..##...##..##..##....
..##..#..#.#....#....#..#.#...#...#....
.#.#..#...#.#...##...#...#.#..##..##...
..#...##...#.#.#.#...##...#....#...#...
..##.#.#....#####.#.#.#...##...##..##..
.#..###.#..#.#.#######.#.#.#..#.#...#..
.#....##....#####...#######....#.#..##.

'''
