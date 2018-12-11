import numpy as np
from scipy import signal
from numpy.fft import fft2, ifft2


def load_grid_serial_number():
    with open('input.txt', encoding='utf-8') as lines:
        return int(next(lines))


def build_power_levels(serial_number):
    grid = np.ones((300, 300), dtype=np.int32)
    x_coord = np.arange(1, 301, 1)
    y_coord = np.arange(1, 301, 1)
    rack_id = grid * x_coord[:, np.newaxis] + 10
    power_level = rack_id * y_coord
    power_level += serial_number
    power_level *= rack_id
    power_level = power_level % 1000 - power_level % 100
    power_level = power_level / 100
    power_level -= 5
    return power_level


def get_highest_energy_cell(power_level, window_size):
    # biggest_window = signal.convolve2d(power_level, np.ones((window_size, window_size)), boundary='symm', mode='same')
    biggest_window = signal.convolve2d(power_level, np.ones((window_size, window_size)), mode='same')
    highest_energy_coords = np.unravel_index(biggest_window.argmax(), biggest_window.shape)

    return highest_energy_coords, biggest_window.max()


def get_highest_energy_cell_in_range(power_level, min_window_size, max_window_size):
    most_highest_energy = -1
    highest_boords = -1
    best_size = -1
    for i in range(min_window_size, max_window_size):
        # print(i)
        highest_energy_coords, highest_energy = get_highest_energy_cell(power_level, i)
        if highest_energy > most_highest_energy:
            highest_boords = highest_energy_coords
            most_highest_energy = highest_energy
            best_size = i
            # print(highest_boords, best_size)
    return (highest_boords[0] - int(best_size / 2) + 1, highest_boords[1] - int(best_size / 2) + 1), best_size


def part_1():
    serial_number = load_grid_serial_number()
    power_level = build_power_levels(serial_number)
    highest_energy_coords, _ = get_highest_energy_cell(power_level, 3)
    print(highest_energy_coords)


def part_2():
    serial_number = load_grid_serial_number()
    power_level = build_power_levels(serial_number)
    most_highest_energy = -1
    most_highest_energy_coords = -1
    highest_window_size = -1

    highest_energy_coords, highest_energy = get_highest_energy_cell(power_level, 13)
    if highest_energy > most_highest_energy:
        most_highest_energy_coords = highest_energy_coords
        most_highest_energy = highest_energy
        highest_window_size = 13
        print(most_highest_energy_coords, highest_window_size)

    for i in range(0, 300):
        print(i)
        highest_energy_coords, highest_energy = get_highest_energy_cell(power_level, i)
        if highest_energy > most_highest_energy:
            most_highest_energy_coords = highest_energy_coords
            most_highest_energy = highest_energy
            highest_window_size = i
            print(most_highest_energy_coords, highest_window_size)
    print(most_highest_energy_coords, highest_window_size)


if __name__ == '__main__':
    from time import time

    start = time()
    assert get_highest_energy_cell(build_power_levels(18), 3)[0] == (33, 45)
    assert get_highest_energy_cell(build_power_levels(42), 3)[0] == (21, 61)
    assert get_highest_energy_cell_in_range(build_power_levels(18), 1, 20) == ((90, 269), 16)
    assert get_highest_energy_cell_in_range(build_power_levels(42), 1, 20) == ((232, 251), 12)
    part_1()
    print(time() - start)

    print(get_highest_energy_cell_in_range(build_power_levels(2187), 1, 30))
    # part_2()
# (238, 45) 13
# 232,39,13
