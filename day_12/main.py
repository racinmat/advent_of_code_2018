import numpy as np


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
            rules[tuple(rule)] = result
    return initial, rules


def calc_next_generation(plants, rules):
    plants = np.pad(plants, 4, 'constant', constant_values=0)
    new_gen_plants = np.zeros_like(plants)
    for i in range(2, len(plants) - 2):
        part = tuple(plants[i - 2:i + 3])
        if part in rules:
            new_gen_plants[i] = rules[part]
    plants_indices = np.where(new_gen_plants == 1)[0]
    plants_start = plants_indices.min()
    plants_end = plants_indices.max()
    return new_gen_plants[plants_start: plants_end+1], plants_start - 4


def part_1():
    initial, rules = load_plants()
    plants = initial
    # print(''.join(map(str, plants)))
    total_offset = 0
    for i in range(0, 1000):
        plants, offset = calc_next_generation(plants, rules)
        total_offset += offset
        # print(''.join(map(str, plants)))
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
