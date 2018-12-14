def load_input():
    with open('input.txt', encoding='utf-8') as lines:
        return int(next(lines))


def part_1():
    num_recipes = load_input()
    board = [3, 7]
    idx_0 = 0
    idx_1 = 1
    for i in range(num_recipes + 10):
        mix = board[idx_0] + board[idx_1]
        mix_results = [int(d) for d in str(mix)]
        # board += mix_results
        board.extend(mix_results)
        idx_0 = (idx_0 + board[idx_0] + 1) % len(board)
        idx_1 = (idx_1 + board[idx_1] + 1) % len(board)
        # print(board)
    print(''.join([str(i) for i in board[num_recipes:num_recipes + 10]]))


def part_2():
    sequence = [int(i) for i in str(load_input())]
    board = [3, 7]
    idx_0 = 0
    idx_1 = 1
    # while board[-len(sequence):] != sequence:
    for i in range(4000000):
        mix = board[idx_0] + board[idx_1]
        mix_results = [int(d) for d in str(mix)]
        board.extend(mix_results)
        idx_0 = (idx_0 + board[idx_0] + 1) % len(board)
        idx_1 = (idx_1 + board[idx_1] + 1) % len(board)
        # print(board)
    print(len(board) - len(sequence))


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
