import numpy as np
from scipy.sparse import csgraph

OCCUPIED = 0
FREE = 1

ELF = 0
GOBLIN = 1


def load_map():
    lines_array = []
    with open('test_input.txt', encoding='utf-8') as lines:
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


def print_grid(grid, unit_locations, units_types):
    string_grid = np.where(grid == FREE, '.', '#')
    elf_locations = unit_locations[units_types == ELF]
    goblin_locations = unit_locations[units_types == GOBLIN]
    string_grid[np.split(elf_locations, [-1], axis=1)] = 'E'
    string_grid[np.split(goblin_locations, [-1], axis=1)] = 'G'

    [print(''.join(i)) for i in string_grid]
    print()


def get_enemy_type(unit_type):
    return 1 - unit_type


def get_free_neighbours(grid, loc):
    neighbours = np.array([
        [-1, 0],
        [1, 0],
        [0, -1],
        [0, 1],
    ], dtype=np.int8)
    neighbours += loc
    neighbours_tuple = neighbours.T[0], neighbours.T[1]
    return neighbours[grid[neighbours_tuple] == FREE]


def get_all_neighbours(grid, loc):
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
        neighbours = get_all_neighbours(grid, free_node)
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


def find_first_step_in_path_to_nearest_target(grid, begin, targets):
    distances = np.ones_like(grid) * np.inf
    distances[tuple(begin)] = 0
    open_nodes = [begin]
    path_found = False
    while not path_found and open_nodes:
        curr = open_nodes.pop(0)
        neighbours = get_free_neighbours(grid, curr)
        neighbours_to_update = neighbours[np.where(distances[tuple(neighbours.T)] > distances[tuple(curr)] + 1)]
        distances[tuple(neighbours_to_update.T)] = distances[tuple(curr)] + 1
        open_nodes.extend(neighbours_to_update)
        targets_in_neighbours = [i in neighbours.tolist() for i in targets.tolist()]
        if np.any(targets_in_neighbours):
            path_found = True

    # can have multiple nearest points, find lexically first
    first_steps = np.where(distances == 1)  # todo: use only distances==1 contained in path
    first_steps = np.array(first_steps).T
    first_step = np.lexsort(np.flip(first_steps.T, 0))[0]    # tiebreak
    return first_steps[first_step]


def find_first_step_in_path_to_nearest_target_dijkstra(grid, begin, targets):
    grid_clear_begin = grid.copy()  # set begin as free node so I can build paths from and to it
    grid_clear_begin[tuple(begin)] = FREE
    adj_matrix = grid_to_adj_matrix(grid_clear_begin)
    grid_csgraph = csgraph.csgraph_from_dense(adj_matrix, null_value=0)

    target_indices = np.ravel_multi_index(targets.T, grid.shape)
    begin_index = np.ravel_multi_index(begin.T, grid.shape)

    dist_matrix, predecessors = csgraph.dijkstra(grid_csgraph, directed=False, indices=begin_index,
                                                 return_predecessors=True)
    target_indices.sort()  # solving tiebreaks by sorting targets so argmin returns correct one
    targets_dists = dist_matrix[target_indices]
    nearest_target = target_indices[np.argmin(targets_dists)]

    paths_indices = get_path_from_predecessors(predecessors, nearest_target)
    path = np.asarray(np.unravel_index(paths_indices, grid.shape)).T
    if path[0].tolist() != begin.tolist():
        return None
    return path


def tick(grid, unit_locations, units_types):
    for i in np.lexsort(np.flip(unit_locations.T, 0)):  # annoying, but this creates correct ordering by coordinates
        unit_loc = unit_locations[i].copy()
        unit_type = units_types[i]
        # unit_loc_tupl = tuple(unit_loc)

        enemy_locations = unit_locations[units_types == get_enemy_type(unit_type)]
        enemy_dists = dist(unit_loc, enemy_locations)
        # moving part, check that no enemy is in neighbourhood and then paths
        if min(enemy_dists) > 1:
            # moving and thus pathfinding is needed
            enemy_neighbours = get_locations_free_neighbours(grid, enemy_locations)  # neighbouring nodes of enemies
            step = find_first_step_in_path_to_nearest_target(grid, unit_loc, enemy_neighbours)
            # todo: check case when no path is feasible and no enemy is reachable
            # is path is None, no feasible path was found
            if step is not None:
                grid[tuple(unit_loc)] = FREE
                unit_loc = step
                grid[tuple(unit_loc)] = OCCUPIED
        # attacking part
        if min(enemy_dists) == 1:
            # todo: implement
            pass
        unit_locations[i] = unit_loc

    return unit_locations, units_types, False


def part_1():
    grid, unit_locations, units_types = load_map()
    print_grid(grid, unit_locations, units_types)
    someone_wins = False
    # while not someone_wins:
    for i in range(5):
        unit_locations, units_types, someone_wins = tick(grid, unit_locations, units_types)
        print_grid(grid, unit_locations, units_types)


def part_2():
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
