import numpy as np
from scipy import signal, ndimage


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
    # sum_window = signal.convolve2d(power_level, np.ones((window_size, window_size)), mode='same')
    # signal.fftconvolve is 1-2 orders of magnitude faster than signal.convolve2d on matrix 300x300
    # signal.fftconvolve is 1-2 orders of magnitude faster than signal.fftconvolve on matrix 300x300
    # signal.fftconvolve is much faster especially for large convolution windows
    # sum_window = ndimage.convolve(power_level, np.ones((window_size, window_size)), mode='constant')
    #
    sum_window = signal.fftconvolve(power_level, np.ones((window_size, window_size)), mode='same')
    highest_energy_coords = np.unravel_index(sum_window.argmax(), sum_window.shape)

    return highest_energy_coords, sum_window.max()


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
    #   indices for signal.convolve2d and signal.fftconvolve
    return (highest_boords[0] - int(best_size / 2) + 1, highest_boords[1] - int(best_size / 2) + 1), best_size
    #   indices for ndimage.convolve
    # return (highest_boords[0] - int(best_size / 2) + 2, highest_boords[1] - int(best_size / 2) + 2), best_size


def part_1():
    serial_number = load_grid_serial_number()
    power_level = build_power_levels(serial_number)
    highest_energy_coords, _ = get_highest_energy_cell(power_level, 3)
    print(highest_energy_coords)


def part_2():
    serial_number = load_grid_serial_number()
    power_level = build_power_levels(serial_number)

    highest_energy_coords, highest_window_size = get_highest_energy_cell_in_range(power_level, 1, 300)
    print(highest_energy_coords, highest_window_size)


if __name__ == '__main__':
    from time import time
    #
    start = time()
    assert get_highest_energy_cell(build_power_levels(18), 3)[0] == (33, 45)
    assert get_highest_energy_cell(build_power_levels(42), 3)[0] == (21, 61)
    assert get_highest_energy_cell_in_range(build_power_levels(18), 1, 40) == ((90, 269), 16)
    assert get_highest_energy_cell_in_range(build_power_levels(42), 1, 40) == ((232, 251), 12)
    part_1()
    part_2()
    print(time() - start)
