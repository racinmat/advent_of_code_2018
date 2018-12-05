def shorten_sequence(sequence: str):
    for i in range(len(sequence) - 1):
        char_1 = sequence[i]
        char_2 = sequence[i + 1]
        if char_1 != char_2 and char_1.lower() == char_2.lower():
            return sequence.replace(char_1 + char_2, '')
    return sequence


if __name__ == '__main__':
    with open('input.txt', encoding='utf-8') as lines:
        sequence = next(lines)

        shorter_sequence = shorten_sequence(sequence)
        while len(shorter_sequence) < len(sequence):
            sequence = shorter_sequence
            shorter_sequence = shorten_sequence(sequence)

    print(len(shorter_sequence))
