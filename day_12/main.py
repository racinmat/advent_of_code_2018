import numpy as np
from scipy import signal, ndimage


def load_plants():
    with open('input.txt', encoding='utf-8') as lines:
        initial = next(lines)[15:].replace('\n', '').replace('#', '1').replace('.', '0')
        initial = list(initial)
        initial = list(map(int, initial))
        next(lines)
        rules = dict()
        for line in lines:
            line = line.replace('\n', '').replace('#', '1').replace('.', '0')
            # line = list(map(int, list(line)))
            rule = list(map(int, line[:5]))
            result = int(line[9:])
            rules[tuple(rule)] = result
    return initial, rules


def calc_next_generation(plants, rules):
    plants = [0, 0, 0, 0] + plants + [0, 0, 0, 0]
    new_gen_plants = [0] * (len(plants))
    for i in range(2, len(plants)-2):
        part = tuple(plants[i - 2:i + 3])
        if part in rules:
            new_gen_plants[i] = rules[part]
    plants_start = new_gen_plants.index(1)
    plants_end = new_gen_plants[::-1].index(1)
    return new_gen_plants[plants_start: len(new_gen_plants) - plants_end], plants_start - 4


def part_1():
    initial, rules = load_plants()
    plants = initial
    print(''.join(map(str, plants)))
    total_offset = 0
    for i in range(0, 1000):
        plants, offset = calc_next_generation(plants, rules)
        total_offset += offset
        # print(''.join(plants))
    plants = np.array(plants)
    # plants_indices = np.where(plants == '#')[0] + total_offset
    plants_indices = np.where(plants == 1)[0] + total_offset
    total_sum = np.sum(plants_indices)
    print(total_sum)

# 187023 is correct answer after 1000 iterations

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