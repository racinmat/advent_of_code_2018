import re
from collections import deque


def load_rules():
    with open('input.txt', encoding='utf-8') as lines:
        line = next(lines)
    m = re.match('(\d+) players; last marble is worth (\d+) points', line)
    num_players = int(m.group(1))
    num_turns = int(m.group(2))
    return num_players, num_turns


def play_game(num_players, num_turns):
    marbles = deque([0])
    scores = [0] * num_players
    curr_player = 1
    for i in range(1, num_turns):
        if i % 23 == 0:
            marbles.rotate(8)
            removed = marbles.popleft()
            scores[curr_player] += i + removed
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(i)

        # some debug printing
        # marbles_print = ['({})'.format(m) if i == current else str(m) for i, m in enumerate(marbles)]
        # print([curr_player], ''.join([str(m).rjust(4) for m in marbles]))
        # if i % 23 == 0:
        #     print(scores)
        curr_player = (curr_player + 1) % num_players
    return scores


def part_1():
    from time import time
    start = time()
    num_players, num_turns = load_rules()

    scores = play_game(num_players, num_turns)

    print(max(scores))
    print(time() - start)


def part_2():
    from time import time
    start = time()
    num_players, num_turns = load_rules()
    num_turns *= 100

    scores = play_game(num_players, num_turns)

    print(max(scores))
    print(time() - start)


if __name__ == '__main__':
    part_1()
    part_2()
