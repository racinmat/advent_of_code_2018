import numpy as np

OCCUPIED = 0
FREE = 1

ELF = 0
GOBLIN = 1


def load_map():
    lines_array = []
    with open('input.txt', encoding='utf-8') as lines:
        for line in lines:
            lines_array.append(list(line.replace('\n', '')))
    string_map = np.array(lines_array)
    grid = np.ones_like(string_map, dtype=np.int8) * 0

    # defining cart things before grid so I can replace those by lines to easier parsing
    units_locations_tuple = np.where(np.isin(string_map, ['E', 'G']))
    units_types = np.where(string_map[units_locations_tuple] == 'E', ELF, GOBLIN)
    unit_locations = np.array(units_locations_tuple).T

    string_map[np.isin(string_map, ['G', 'E'])] = '#'

    grid[string_map == '#'] = OCCUPIED
    grid[string_map == '.'] = FREE

    return grid, unit_locations, units_types


def print_grid(grid, unit_locations, units_types, unit_hps):
    string_grid = np.where(grid == FREE, '.', '#')
    elf_locations = unit_locations[(units_types == ELF) & (unit_hps > 0)]
    goblin_locations = unit_locations[(units_types == GOBLIN) & (unit_hps > 0)]
    string_grid[np.split(elf_locations, [-1], axis=1)] = 'E'
    string_grid[np.split(goblin_locations, [-1], axis=1)] = 'G'

    [print(''.join(i)) for i in string_grid]
    [print('E' if units_types[i] == ELF else 'G', unit_locations[i], unit_hps[i]) for i in range(len(units_types))]
    print()


def get_enemy_type(unit_type):
    return 1 - unit_type


def get_free_neighbours(grid, loc):
    neighbours = get_all_neighbours(loc)
    neighbours_tuple = neighbours.T[0], neighbours.T[1]
    return neighbours[grid[neighbours_tuple] == FREE]


def get_type_neighbours(loc, type, unit_locations, unit_types):
    neighbours = get_all_neighbours(loc)
    return np.array([n for n in neighbours if n.tolist() in unit_locations[unit_types == type].tolist()])


def get_all_neighbours(loc):
    neighbours = np.array([
        [-1, 0],
        [1, 0],
        [0, -1],
        [0, 1],
    ], dtype=np.int8)
    neighbours += loc
    return neighbours


def dist(loc, locations):
    return np.sum(np.abs(locations - loc), axis=1)


def grid_to_adj_matrix(grid):
    indices = np.indices(grid.shape)
    flat_indices = np.ravel_multi_index(indices, grid.shape)
    adj_matrix = np.zeros((flat_indices.max() + 1, flat_indices.max() + 1), dtype=np.int8)
    free_nodes = np.asarray(np.where(grid == FREE))
    free_node_indices = np.ravel_multi_index(free_nodes, grid.shape)
    for free_node, free_index in zip(free_nodes.T, free_node_indices):
        neighbours = get_all_neighbours(free_node)
        neighbour_indices = np.ravel_multi_index(neighbours.T, grid.shape)

        adj_matrix[neighbour_indices, [free_index]] = 1
    # I can get to free node from its each neighbour
    # todo: benchmark doing every neighbour to free and then symmetrizing, compared to free neighbours to all free nodes, which is already symmetric
    return adj_matrix & adj_matrix.T  # symmetrize the matrix


def get_locations_free_neighbours(grid, locations):
    all_neighbours = np.empty((0, 2), dtype=np.int8)
    for location in locations:
        neighbours = get_free_neighbours(grid, location)
        all_neighbours = np.concatenate((all_neighbours, neighbours))
    return all_neighbours


def get_path_from_predecessors(predecessors_matrix, target):
    no_path = predecessors_matrix.min()
    path = [target]
    curr = target
    while predecessors_matrix[curr] != no_path:
        curr = predecessors_matrix[curr]
        path.append(curr)
    path.reverse()
    return path


def first_in_reading_order(arr):
    index = np.lexsort(np.flip(arr.T, 0))[0]
    return arr[index], index


def find_first_step_in_path_to_nearest_target(grid, begin, targets):
    distances = np.ones_like(grid, np.int32) * 20000    # should be big enough to behave like infinity
    distances[tuple(begin)] = 0
    open_nodes = [begin]
    path_found = False
    targets_in_neighbours = []
    predecessors = dict()
    while not path_found and open_nodes:
        updated_neighbours = set()
        for node in open_nodes:
            neighbours = get_free_neighbours(grid, node)
            neighbours_to_update = neighbours[np.where(distances[tuple(neighbours.T)] >= distances[tuple(node)] + 1)]
            updated_neighbours = updated_neighbours.union(set([tuple(i.tolist()) for i in neighbours_to_update]))
            for n in neighbours_to_update:
                n = tuple(n)
                if n not in predecessors:
                    predecessors[n] = set()
                predecessors[n].add(tuple(node))
            distances[tuple(neighbours_to_update.T)] = distances[tuple(node)] + 1

        open_nodes = updated_neighbours
        targets_in_neighbours = [tuple(i) in updated_neighbours for i in targets.tolist()]
        if np.any(targets_in_neighbours):
            path_found = True

    nearest_targets = targets[targets_in_neighbours]
    if len(nearest_targets) == 0:
        return None

    nearest_target, _ = first_in_reading_order(nearest_targets)

    curr_nodes = [tuple(nearest_target)]
    while True:
        previous_nodes = [j for i in curr_nodes for j in predecessors[i]]
        if tuple(begin) in previous_nodes:
            break
        curr_nodes = previous_nodes
    next_step_nodes = curr_nodes

    next_step_node, _ = first_in_reading_order(np.array(next_step_nodes))
    return next_step_node


def tick(grid, unit_locations, unit_types, unit_hps, unit_attacks):
    for i in np.lexsort(np.flip(unit_locations.T, 0)):  # annoying, but this creates correct ordering by coordinates
        if unit_hps[i] <= 0:
            continue

        unit_loc = unit_locations[i].copy()
        unit_type = unit_types[i]

        enemy_locations = unit_locations[(unit_types == get_enemy_type(unit_type)) & (unit_hps > 0)]

        if len(enemy_locations) == 0:
            return unit_locations, unit_types, unit_hps, unit_attacks, True, False

        enemy_dists = dist(unit_loc, enemy_locations)
        # moving part, check that no enemy is in neighbourhood and then paths
        if min(enemy_dists) > 1:
            # moving and thus pathfinding is needed
            enemy_neighbours = get_locations_free_neighbours(grid, enemy_locations)  # neighbouring nodes of enemies
            step = find_first_step_in_path_to_nearest_target(grid, unit_loc, enemy_neighbours)
            # is path is None, no feasible path was found
            if step is not None:
                grid[tuple(unit_loc)] = FREE
                unit_loc = step
                grid[tuple(unit_loc)] = OCCUPIED

            unit_locations[i] = unit_loc

        enemy_dists = dist(unit_loc, enemy_locations)  # recalculate after movement
        # attacking part
        if min(enemy_dists) == 1:
            adjacent_enemies = get_type_neighbours(unit_loc, get_enemy_type(unit_type), unit_locations, unit_types)
            adjacent_enemy_indices = [i in adjacent_enemies.tolist() for i in unit_locations.tolist()]
            min_living_hp = unit_hps[adjacent_enemy_indices & (unit_hps > 0)].min()
            min_adjacent_enemy_health_indices = adjacent_enemy_indices & (unit_hps == min_living_hp)
            enemies_to_attack = unit_locations[min_adjacent_enemy_health_indices]
            enemy_to_attack, index = first_in_reading_order(enemies_to_attack)
            enemy_to_attack_index = np.where(min_adjacent_enemy_health_indices)[0][index]

            unit_hps[enemy_to_attack_index] -= unit_attacks[i]
            if unit_hps[enemy_to_attack_index] <= 0:
                grid[tuple(enemy_to_attack)] = FREE  # setting dead unit position to be free

    someone_won = unit_hps[unit_types == GOBLIN].max() <= 0 or unit_hps[unit_types == ELF].max() <= 0
    return unit_locations, unit_types, unit_hps, unit_attacks, someone_won, True


def part_1():
    grid, unit_locations, units_types = load_map()
    unit_hps = np.ones_like(units_types) * 200
    unit_attacks = np.ones_like(units_types) * 3
    # print_grid(grid, unit_locations, units_types, unit_hps)
    someone_wins = False
    num_rounds = 0
    while not someone_wins:
        unit_locations, units_types, unit_hps, unit_attacks, someone_wins, full_turn = tick(
            grid, unit_locations, units_types, unit_hps, unit_attacks)
        if full_turn:
            num_rounds += 1
        print('round ', num_rounds)
        # print_grid(grid, unit_locations, units_types, unit_hps)

    # print(num_rounds)
    # print(unit_hps[unit_hps > 0].sum())
    print(unit_hps[unit_hps > 0].sum() * num_rounds)


def part_2():
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
