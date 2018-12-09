import re


def add_marble(i, current):
    position = (current + 2) % len(marbles)
    if position == 0:
        position = len(marbles)
    marbles.insert(position, i)
    return position


if __name__ == '__main__':
    with open('test_input.txt', encoding='utf-8') as lines:
        line = next(lines)
    m = re.match('(\d+) players; last marble is worth (\d+) points', line)
    num_players = int(m.group(1))
    num_turns = int(m.group(2))

    marbles = [0]
    scores = [0] * num_players
    current = 1
    curr_player = 1
    for i in range(1, num_turns):
        if i % 23 == 0:
            removed_idx = (current - 7) % len(marbles)
            removed = marbles.pop(removed_idx)
            current = removed_idx
            scores[curr_player] += 23 + removed
        else:
            current = add_marble(i, current)

        # marbles_print = ['({})'.format(m) if i == current else str(m) for i, m in enumerate(marbles)]
        # print([curr_player], ''.join([m.rjust(4) for m in marbles_print]))
        # if i % 23 == 0:
        #     print(scores)
        curr_player = (curr_player + 1) % num_players

    print(max(scores))
