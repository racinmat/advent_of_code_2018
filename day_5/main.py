def invert(char: str):
    return char.upper() if char.islower() else char.lower()


def shorten_sequence(sequence: str):
    stack = []
    for char in sequence:
        if stack:  # empty check
            if char == invert(stack[-1]):
                stack.pop()
            else:
                stack.append(char)
        else:
            stack.append(char)
    return ''.join(stack)


def load_sequence():
    with open('input.txt', encoding='utf-8') as lines:
        sequence = next(lines)  # type: str
    return sequence


def part_1():
    sequence = load_sequence()
    sequence = shorten_sequence(sequence)
    print(len(sequence))


def part_2():
    sequence = load_sequence()
    unique_chars = ''.join(set(sequence.lower()))

    lengths = dict()
    for unique_char in unique_chars:
        shorter_sequence = shorten_sequence(sequence.replace(unique_char.lower(), '').replace(unique_char.upper(), ''))

        lengths[unique_char] = len(shorter_sequence)
    print(min(lengths.values()))


if __name__ == '__main__':
    part_1()
    part_2()
