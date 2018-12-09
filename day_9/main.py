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
    for i in range(1, num_turns + 1):
        if i % 23 == 0:
            marbles.rotate(7)
            removed = marbles.pop()
            scores[i % num_players] += i + removed
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(i)

        # some debug printing
        # print([curr_player], ''.join([str(m).rjust(4) for m in marbles]))
        # if i % 23 == 0:
        #     print(scores)
    return max(scores)


def play_game_2(max_players, last_marble):
    scores = [0] * max_players
    circle = deque([0])

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % max_players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores)


def part_1():
    # from time import time
    # start = time()
    num_players, num_turns = load_rules()

    max_score = play_game(num_players, num_turns)

    print(max_score)
    # print(time() - start)


def part_2():
    # from time import time
    # start = time()
    num_players, num_turns = load_rules()
    num_turns *= 100

    max_score = play_game(num_players, num_turns)

    print(max_score)
    # print(time() - start)


if __name__ == '__main__':
    part_1()
    part_2()
