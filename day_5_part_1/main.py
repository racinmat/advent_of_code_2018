def invert(char: str):
    return char.upper() if char.islower() else char.lower()


def shorten_sequence(sequence: str):
    stack = []
    for char in sequence:
        if stack:   # empty check
            if char == invert(stack[-1]):
                stack.pop()
            else:
                stack.append(char)
        else:
            stack.append(char)
    return ''.join(stack)


if __name__ == '__main__':
    with open('input.txt', encoding='utf-8') as lines:
        sequence = next(lines)  # type: str
    sequence = shorten_sequence(sequence)
    print(len(sequence))
