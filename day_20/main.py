import re
import numpy as np

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

m = {
    'W': LEFT,
    'E': RIGHT,
    'N': UP,
    'S': DOWN,
}

MOVE = {
    LEFT: [0, -1],
    UP: [-1, 0],
    RIGHT: [0, 1],
    DOWN: [1, 0],
}


def load_input() -> str:
    with open('test_input.txt', encoding='utf-8') as lines:
        regex = next(lines)
    return regex


def prepare_data():
    regex = load_input()
    count_w = regex.count('W')
    count_e = regex.count('E')
    count_n = regex.count('N')
    count_s = regex.count('S')
    max_width = count_w + count_e
    max_height = count_n + count_s
    grid = np.zeros((max_height, max_width, 4))
    pos = np.array([count_w, count_n])
    return regex, grid, pos


def explore_branches(grid, branches):
    # todo: implement me
    pass

def process_straight_path(grid, path, pos):
    # todo: implement me
    # přesunout sem nějaké věci z explore path
    pass


def explore_path(grid, path, pos):
    #     todo: dodělat
    # idea: explore_path bude přijímat string s nějakou cestou, kterou prozkoumá, najde v ní všechny branche hloubky 1 a prozkoumá je
    # explore_branches si bude pamatovat start a z něj projde všechny možnosti pomocí explore_path
    # zanořené branche se vyřeší tím, že explore_branches bude volat explore_path
    path_pos = 0
    curr_pos = pos
    while path_pos < len(path):
        letter = path[path_pos]
        if letter == '^':
            path_pos += 1
            continue

        path_end = path_pos + path[path_pos:].find('(')
        for letter in path[path_pos:path_end]:
            course = m[letter]
            grid[curr_pos, course] = 1
            pos += MOVE[course]
        path_pos = path_end

        depth = 0
        # branches finding
        branches_start = path_end
        branches_end = None
        for i, letter in enumerate(path[branches_start:]):
            if letter == '(':
                depth += 1
                continue
            if letter == ')':
                depth -= 1
            if depth == 0:
                branches_end = branches_start + i + 1
                break

        explore_branches(grid, path[branches_start:branches_end])
        path_pos = branches_end

    pass


def part_1():
    regex, grid, pos = prepare_data()
    explore_path(grid, regex, pos)


def part_2():
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
