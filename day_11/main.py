import re
import numpy as np
from PIL import Image
from scipy import signal


def load_grid_serial_number():
    with open('input.txt', encoding='utf-8') as lines:
        return int(next(lines))


def part_1():
    serial_number = load_grid_serial_number()
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
    biggest_window = signal.convolve2d(power_level, np.ones((3, 3)), boundary='symm', mode='same')
    print(biggest_window)
    highest_energy = np.unravel_index(biggest_window.argmax(), biggest_window.shape)
    print(highest_energy)


def part_2():
    pass


if __name__ == '__main__':
    part_1()
    part_2()
# 66,136