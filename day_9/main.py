import re


def load_rules():
    with open('input.txt', encoding='utf-8') as lines:
        line = next(lines)
    m = re.match('(\d+) players; last marble is worth (\d+) points', line)
    num_players = int(m.group(1))
    num_turns = int(m.group(2))
    return num_players, num_turns


def add_marble(i, current, marbles):
    position = (current + 2) % len(marbles)
    if position == 0:
        position = len(marbles)
    marbles.insert(position, i)
    return position


def play_game(num_players, num_turns):
    marbles = [0]
    scores = [0] * num_players
    current = 1
    curr_player = 1
    for i in range(1, num_turns):
        if i % 23 == 0:
            removed_idx = (current - 7) % len(marbles)
            removed = marbles.pop(removed_idx)
            current = removed_idx
            scores[curr_player] += i + removed
        else:
            current = add_marble(i, current, marbles)

        # some debug printing
        # marbles_print = ['({})'.format(m) if i == current else str(m) for i, m in enumerate(marbles)]
        # print([curr_player], ''.join([m.rjust(4) for m in marbles_print]))
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
    # part_2()
