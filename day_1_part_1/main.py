if __name__ == '__main__':
    total = 0
    with open('input.txt') as lines:
        for line in lines:
            total += int(line)
    print(total)
