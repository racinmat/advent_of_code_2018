def load_input():
    changes = []
    with open('input.txt', encoding='utf-8') as lines:
        change = None
        stop_counter = 0
        for i, line in enumerate(lines):
            if line == '\n':
                stop_counter += 1
            else:
                stop_counter = 0
            if stop_counter >= 3:
                break
            if line == '\n':
                continue
            if i % 4 == 0:
                registry_before = [int(i) for i in line.replace('\n', '')[9:-1].split(', ')]
                change = {'before': registry_before}
            elif i % 4 == 1:
                instruction = [int(i) for i in line.replace('\n', '').split(' ')]
                change['instruction'] = instruction
            elif i % 4 == 2:
                registry_after = [int(i) for i in line.replace('\n', '')[9:-1].split(', ')]
                change['after'] = registry_after
                changes.append(change)
    return changes


def apply_addr(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = registry[a] + registry[b]
    return registry


def apply_addi(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = registry[a] + b
    return registry


def apply_mulr(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = registry[a] * registry[b]
    return registry


def apply_muli(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = registry[a] * b
    return registry


def apply_banr(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = registry[a] & registry[b]
    return registry


def apply_bani(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = registry[a] & b
    return registry


def apply_borr(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = registry[a] | registry[b]
    return registry


def apply_bori(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = registry[a] | b
    return registry


def apply_setr(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = registry[a]
    return registry


def apply_seti(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = a
    return registry


def apply_gtir(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = 1 if a > registry[b] else 0
    return registry


def apply_gtri(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = 1 if registry[a] > b else 0
    return registry


def apply_gtrr(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = 1 if registry[a] > registry[b] else 0
    return registry


def apply_eqir(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = 1 if a == registry[b] else 0
    return registry


def apply_eqri(params, registry):
    a, b, c = params
    registry = registry[:]
    registry[c] = 1 if registry[a] == b else 0
    return registry


def apply_eqrr(params, registry):
    a, b, c = params
    registry = 1 if registry[a] == registry[b] else 0
    return registry


def part_1():
    change_logs = load_input()
    instructions = {
        'addr': apply_addr,
        'addi': apply_addi,
        'mulr': apply_mulr,
        'muli': apply_muli,
        'banr': apply_banr,
        'bani': apply_bani,
        'borr': apply_borr,
        'bori': apply_bori,
        'setr': apply_setr,
        'seti': apply_seti,
        'gtir': apply_gtir,
        'gtri': apply_gtri,
        'gtrr': apply_gtrr,
        'eqir': apply_eqir,
        'eqri': apply_eqri,
        'eqrr': apply_eqrr,
    }

    # set possible mapping to everything and remove not right mappings
    possible_mappings = [set(instructions.keys()) for i in range(16)]

    num_at_least_three_opcodes = 0
    for change_log in change_logs:
        before = change_log['before']
        instruction = change_log['instruction']
        instr_num = instruction[0]
        params = instruction[1:]
        after = change_log['after']
        valid_instructions = [instruction for instruction, fun in instructions.items() if fun(params, before) == after]
        if len(valid_instructions) >= 3:
            num_at_least_three_opcodes += 1
        # possible_mappings[instr_num] = possible_mappings[instr_num].intersection(set(valid_instructions))

    print(num_at_least_three_opcodes)

# guessed 3
def part_2():
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)