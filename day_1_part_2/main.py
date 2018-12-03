if __name__ == '__main__':
    changes = []
    with open('../day_1_part_1/input.txt') as lines:
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
