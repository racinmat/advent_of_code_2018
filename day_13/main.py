import numpy as np

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

MOVE = {
    LEFT: [0, -1],
    UP: [-1, 0],
    RIGHT: [0, 1],
    DOWN: [1, 0],
}

NEXT_TIEBREAK = {
    0: 1,
    1: -1,
    -1: 0,
}


def load_map():
    lines_array = []
    with open('test_input.txt', encoding='utf-8') as lines:
        for line in lines:
            lines_array.append(list(line.replace('\n', '')))
    string_map = np.array(lines_array)
    grid = np.ones(string_map.shape + (4,), dtype=np.int8) * 0

    # defining cart things before grid so I can replace those by lines to easier parsing
    cart_locations_tuple = np.where(np.isin(string_map, ['>', '^', 'v', '<']))
    cart_locations = np.array(cart_locations_tuple).T
    cart_directions = (string_map[cart_locations_tuple] == '>') * RIGHT + \
                      (string_map[cart_locations_tuple] == '^') * UP + \
                      (string_map[cart_locations_tuple] == '<') * LEFT + \
                      (string_map[cart_locations_tuple] == 'v') * DOWN
    cart_next_tiebreaks = np.ones_like(cart_directions) * -1    # first tiebreak is turning left

    string_map[np.isin(string_map, ['<', '>'])] = '-'
    string_map[np.isin(string_map, ['^', 'v'])] = '|'

    grid[string_map == '|', UP] = 1
    grid[string_map == '|', DOWN] = 1

    grid[string_map == '-', LEFT] = 1
    grid[string_map == '-', RIGHT] = 1

    grid[string_map == '+', :] = 1

    grid[(string_map == '/') & (np.isin(np.roll(string_map, -1, axis=1), ['-', '+'])), RIGHT] = 1
    grid[(string_map == '/') & (np.isin(np.roll(string_map, -1, axis=0), ['|', '+'])), DOWN] = 1
    grid[(string_map == '/') & (np.isin(np.roll(string_map, 1, axis=1), ['-', '+'])), LEFT] = 1
    grid[(string_map == '/') & (np.isin(np.roll(string_map, 1, axis=0), ['|', '+'])), UP] = 1

    grid[(string_map == '\\') & (np.isin(np.roll(string_map, -1, axis=1), ['-', '+'])), RIGHT] = 1
    grid[(string_map == '\\') & (np.isin(np.roll(string_map, 1, axis=0), ['|', '+'])), UP] = 1
    grid[(string_map == '\\') & (np.isin(np.roll(string_map, 1, axis=1), ['-', '+'])), LEFT] = 1
    grid[(string_map == '\\') & (np.isin(np.roll(string_map, -1, axis=0), ['|', '+'])), DOWN] = 1

    return grid, cart_locations, cart_directions, cart_next_tiebreaks


class CollisionException(RuntimeError):
    pass


def print_grid(grid, cart_locations, cart_directions):
    print_map = np.array(['-', '|', '-', '|'])
    string_grid = print_map[np.argmax(grid, axis=-1)]
    string_grid[(grid[:, :, DOWN] & grid[:, :, RIGHT]) == 1] = '/'
    string_grid[(grid[:, :, UP] & grid[:, :, LEFT]) == 1] = '/'

    string_grid[(grid[:, :, DOWN] & grid[:, :, LEFT]) == 1] = '\\'
    string_grid[(grid[:, :, UP] & grid[:, :, RIGHT]) == 1] = '\\'

    string_grid[grid.sum(axis=-1) == 4] = '+'

    string_grid[grid.sum(axis=-1) == 0] = ' '

    for i, ch in {LEFT: '<', RIGHT: '>', UP: '^', DOWN: 'v'}.items():
        string_grid[np.split(cart_locations[cart_directions == i], [-1], axis=1)] = ch

    [print(''.join(i)) for i in string_grid]
    # todo: dodělat
    print()


def tick(grid, cart_locations, cart_directions, cart_next_tiebreaks):
    for i in np.lexsort(cart_locations):
        cart_loc = cart_locations[i].copy()
        cart_loc_tupl = tuple(cart_locations[i])
        cart_dir = cart_directions[i]
        tiebreak = cart_next_tiebreaks[i]
        map_pos = grid[cart_loc_tupl]
        if map_pos.sum() <= 2:  # continue
            same_dir = grid[cart_loc_tupl + (cart_dir,)]
            if same_dir:
                cart_loc += MOVE[cart_dir]
            else:
                indices = np.indices(map_pos.shape)
                available_dirs = (indices >= cart_dir - 1) & (indices <= cart_dir + 1) * map_pos
                new_dir = np.argmax(map_pos & available_dirs)
                cart_loc += MOVE[new_dir]
                cart_dir = new_dir
        else:  # intersection
            new_cart_dir = (cart_dir + tiebreak) % 4
            cart_loc += MOVE[new_cart_dir]
            cart_next_tiebreaks[i] = NEXT_TIEBREAK[tiebreak]
            cart_dir = new_cart_dir
        if cart_loc.tolist() in cart_locations.tolist():
            raise CollisionException(cart_loc)
        cart_locations[i] = cart_loc
        cart_directions[i] = cart_dir


def part_1():
    grid, cart_locations, cart_directions, cart_next_tiebreaks = load_map()
    print_grid(grid, cart_locations, cart_directions)
    try:
        # while True:
        for i in range(20):
            tick(grid, cart_locations, cart_directions, cart_next_tiebreaks)
            print_grid(grid, cart_locations, cart_directions)
    #         todo: add printing
    except CollisionException as e:
        print(e.message)


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
