import re
import numpy as np

CLAY = -1
FREE = 1
WATER = 2

def load_input():
    clays = []
    with open('test_input.txt', encoding='utf-8') as lines:
        for line in lines:
            m = re.match('([xy])=(\d+)\.?\.?(\d+)?, ([xy])=(\d+)\.?\.?(\d+)?', line.replace('\n', ''))
            g = m.groups()
            coord_1 = g[0]
            range_1 = int(g[1]) if g[2] is None else range(int(g[1]), int(g[2]) + 1)# from inclusive to exclusive range
            coord_2 = g[3]
            range_2 = int(g[4]) if g[5] is None else range(int(g[4]), int(g[5]) + 1)# from inclusive to exclusive range
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


def get_valid_instructions(change_log, instructions):
    before = change_log['before']
    instruction = change_log['instruction']
    instr_num = instruction[0]
    params = instruction[1:]
    after = change_log['after']
    valid_instructions = [instruction for instruction, fun in instructions.items() if fun(params, before) == after]
    return valid_instructions, instr_num


def part_1():
    change_logs, instructions, _ = prepare_data()
    pass


def part_2():
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
