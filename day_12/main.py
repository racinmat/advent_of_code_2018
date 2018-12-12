import numpy as np
from scipy import signal, ndimage


def load_plants():
    with open('test_input.txt', encoding='utf-8') as lines:
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
    plants = ['.', '.'] + plants + ['.', '.']
    new_gen_plants = ['.'] * (len(plants))
    for i in range(2, len(plants)):
        part = tuple(plants[i - 2:i + 3])
        if part in rules:
            new_gen_plants[i] = rules[part]
    plants_start = new_gen_plants.index('#')
    plants_end = new_gen_plants[::-1].index('#')
    return new_gen_plants[plants_start: len(new_gen_plants) - plants_end]
    # return new_gen_plants


def part_1():
    initial, rules = load_plants()
    plants = initial
    print(''.join(plants))
    for i in range(0, 100):
        plants = calc_next_generation(plants, rules)
        print(''.join(plants))


def part_2():
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)

'''
...#..#.#..##......###...###
...#...#....#.....#..#..#..#
...##..##...##....#..#..#..#
...#...#..#.#....#..#..#..#
...##..#...#.#...#..#..#..#
...#..##...#.#..#..#..#..#
...#...#....#...#..#..#..#
...##..##...##..#..#..#..#
...#...#..#.#..#..#..#..#
...##..#...#...#..#..#..#
...#..##..##..#..#..#..#
...#...#...#..#..#..#..#
...##..##..#..#..#..#..#
...#...#..#..#..#..#..#
...##..#..#..#..#..#..#
...#..#..#..#..#..#..#
...#..#..#..#..#..#..#
...#..#..#..#..#..#..#
...#..#..#..#..#..#..#
...#..#..#..#..#..#..#
...#..#..#..#..#..#..#

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