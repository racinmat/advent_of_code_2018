def shorten_sequence_once(sequence: str):
    for i in range(len(sequence) - 1):
        char_1 = sequence[i]
        char_2 = sequence[i + 1]
        if char_1 != char_2 and char_1.lower() == char_2.lower():
            return sequence.replace(char_1 + char_2, '')
    return sequence


def shorten_sequence(sequence: str):
    shorter_sequence = shorten_sequence_once(sequence)
    while len(shorter_sequence) < len(sequence):
        sequence = shorter_sequence
        shorter_sequence = shorten_sequence_once(sequence)
    return shorter_sequence


if __name__ == '__main__':
    with open('../day_5_part_1/input.txt', encoding='utf-8') as lines:
        sequence = next(lines)  # type: str
    unique_chars = ''.join(set(sequence.lower()))

    lengths = dict()
    for char in unique_chars:
        shorter_sequence = shorten_sequence(sequence.replace(char.lower(), '').replace(char.upper(), ''))

        lengths[char] = len(shorter_sequence)
    print(min(lengths.values()))
