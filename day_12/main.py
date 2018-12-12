import numpy as np
from scipy import signal, ndimage


def load_plants():
    with open('input.txt', encoding='utf-8') as lines:
        initial = next(lines)[15:].replace('\n', '')
        initial = list(initial)
        next(lines)
        rules = dict()
        for line in lines:
            line = line.replace('\n', '')
            rule = line[:5]
            result = line[9:]
            rules[tuple(rule)] = result
    return initial, rules


def calc_next_generation(plants, rules):
    plants = ['.', '.', '.', '.'] + plants + ['.', '.', '.', '.']
    new_gen_plants = ['.'] * (len(plants))
    for i in range(2, len(plants)-2):
        part = tuple(plants[i - 2:i + 3])
        if part in rules:
            new_gen_plants[i] = rules[part]
    plants_start = new_gen_plants.index('#')
    plants_end = new_gen_plants[::-1].index('#')
    return new_gen_plants[plants_start: len(new_gen_plants) - plants_end], plants_start - 4
    # return new_gen_plants


def part_1():
    initial, rules = load_plants()
    plants = initial
    print(''.join(plants))
    total_offset = 0
    for i in range(0, 1000):
        plants, offset = calc_next_generation(plants, rules)
        total_offset += offset
        # print(''.join(plants))
    plants = np.array(plants)
    plants_indices = np.where(plants == '#')[0] + total_offset
    total_sum = np.sum(plants_indices)
    print(total_sum)

def part_2():
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

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