import re
import numpy as np

FREE = 0
WALL = 1

MOVE = {
    'W': [0, -1],
    'E': [0, 1],
    'N': [-1, 0],
    'S': [1, 0],
}


def load_input() -> str:
    with open('input.txt', encoding='utf-8') as lines:
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
    grid = np.ones((max_height * 2 + 1, max_width * 2 + 1), np.int32)
    pos = np.array([count_w * 2, count_n * 2])

    grid[tuple(pos)] = FREE
    return regex, grid, pos


#  todo: fix on test input, branch in right bottom is not correct
def explore_branches(grid, branches_string, start_pos):
    # can't split only by .split('|') because I need to use only splits in depth 1
    split_indices = [0]
    depth = 0
    for i, letter in enumerate(branches_string):
        if letter == '(':
            depth += 1
        if letter == ')':
            depth -= 1
        if depth == 1 and letter == '|':
            split_indices.append(i)

    branches = [branches_string[i + 1:j] for i, j in zip(split_indices, split_indices[1:] + [-1])]
    # branches = branches_string[1:-1].split('|')
    for branch in branches:
        if branch == '':
            continue
        process_path(grid, branch, start_pos.copy())


def process_straight_path(grid, path, curr_pos):
    for letter in path:
        curr_pos += MOVE[letter]
        grid[tuple(curr_pos)] = FREE
        curr_pos += MOVE[letter]
        grid[tuple(curr_pos)] = FREE
    return curr_pos


def process_path(grid, path, pos):
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

        if letter == '$':
            break

        branches_start_pos = path[path_pos:].find('(')

        if branches_start_pos == -1:
            curr_pos = process_straight_path(grid, path[path_pos:], curr_pos)
            break
        else:
            path_end = path_pos + branches_start_pos
            curr_pos = process_straight_path(grid, path[path_pos:path_end], curr_pos)

        # print_grid(grid, curr_pos)

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

        explore_branches(grid, path[branches_start:branches_end], curr_pos)
        path_pos = branches_end

        # print_grid(grid, curr_pos)
    return grid


def print_grid(grid, pos):
    y_vals, x_vals = np.where(grid == FREE)[0:2]
    min_y, max_y = min(y_vals) - 1, max(y_vals) + 1
    min_x, max_x = min(x_vals) - 1, max(x_vals) + 1

    grid_to_print = grid[min_y:max_y + 1, min_x:max_x + 1]

    string_grid = np.chararray(grid_to_print.shape, unicode=True)
    string_grid[grid_to_print == FREE] = '.'
    string_grid[grid_to_print == WALL] = '#'
    string_grid[tuple(pos - [min_y, min_x])] = 'X'

    [print(''.join(i)) for i in string_grid]
    print()


def get_all_neighbours(loc):
    neighbours = np.array([
        [-1, 0],
        [1, 0],
        [0, -1],
        [0, 1],
    ], dtype=np.int32)
    neighbours += loc
    return neighbours


def get_free_neighbours(grid, loc):
    neighbours = get_all_neighbours(loc)
    neighbours_tuple = neighbours.T[0], neighbours.T[1]
    return neighbours[grid[neighbours_tuple] == FREE]


def get_free_neighbours_for_locations(grid, locs):
    neighbours = np.concatenate([get_all_neighbours(loc) for loc in locs])
    neighbours_tuple = neighbours.T[0], neighbours.T[1]
    return neighbours[grid[neighbours_tuple] == FREE]


def calculate_all_distances_from_position(grid, start_pos):
    distances = np.ones_like(grid, np.int32) * 200000  # should be big enough to behave like infinity
    distances[tuple(start_pos)] = 0
    open_nodes = [start_pos]
    # some slightly modified dijkstra, boi
    curr_dist = 0
    while len(open_nodes) > 0:
        neighbours = get_free_neighbours_for_locations(grid, open_nodes)
        # changing this line gives different results, tiebreaking in dijkstra looks broken, fix it
        neighbours_to_update = neighbours[np.where(distances[tuple(neighbours.T)] >= curr_dist + 1)]
        # neighbours_to_update = neighbours[np.where(distances[tuple(neighbours.T)] > distances[tuple(node)] + 1)]
        updated_neighbours = neighbours_to_update
        distances[tuple(neighbours_to_update.T)] = curr_dist + 1

        open_nodes = updated_neighbours
        curr_dist += 1

    distances[distances == 200000] = -1
    return distances


def part_1():
    regex, grid, start_pos = prepare_data()
    grid = process_path(grid, regex, start_pos.copy())
    print_grid(grid, start_pos)

    y_vals, x_vals = np.where(grid == FREE)[0:2]
    min_y, max_y = min(y_vals) - 1, max(y_vals) + 1
    min_x, max_x = min(x_vals) - 1, max(x_vals) + 1
    grid = grid[min_y:max_y + 1, min_x:max_x + 1]

    distances = calculate_all_distances_from_position(grid, start_pos - [min_y, min_x])
    print(int(np.round(distances.max() / 2)))

# 9367 too high
def part_2():
    regex, grid, start_pos = prepare_data()
    grid = process_path(grid, regex, start_pos.copy())
    print_grid(grid, start_pos)

    y_vals, x_vals = np.where(grid == FREE)[0:2]
    min_y, max_y = min(y_vals) - 1, max(y_vals) + 1
    min_x, max_x = min(x_vals) - 1, max(x_vals) + 1
    grid = grid[min_y:max_y + 1, min_x:max_x + 1]

    distances = calculate_all_distances_from_position(grid, start_pos - [min_y, min_x])
    print(int(np.round(np.sum(distances >= 1000 * 2) / 2)))


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
