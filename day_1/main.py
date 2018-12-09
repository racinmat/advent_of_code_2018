def part_1():
    total = 0
    with open('input.txt') as lines:
        for line in lines:
            total += int(line)
    print(total)


def part_2():
    changes = []
    with open('input.txt') as lines:
        for line in lines:
            changes.append(int(line))

    frequencies = {0}
    curr_freq = 0
    found = False
    while not found:
        for change in changes:
            curr_freq += change
            if curr_freq in frequencies:
                found = True
                break
            frequencies.add(curr_freq)

    print(curr_freq)


if __name__ == '__main__':
    part_1()
    part_2()
