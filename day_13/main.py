import numpy as np


def load_map():
    lines_array = []
    with open('test_input.txt', encoding='utf-8') as lines:
        for line in lines:
            lines_array.append(list(line.replace('\n', '')))
    map = np.array(lines_array)
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
    initial, rules = load_map()
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


def part_2():
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)

'''
In this example, the location of the first crash is 7,3.
'''
