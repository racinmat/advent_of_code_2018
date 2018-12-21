import re


def load_input():
    program = []
    with open('input.txt', encoding='utf-8') as lines:
        m = re.match('#ip (\d+)', next(lines))
        ip = int(m.group(1))
        for i, line in enumerate(lines):
            instruction_parts = line.replace('\n', '').split(' ')
            instruction_name = instruction_parts[0]
            program.append((instruction_name, [int(i) for i in instruction_parts[1:]]))
    return ip, program


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
    registry[c] = 1 if registry[a] == registry[b] else 0
    return registry


def prepare_data():
    ip, program = load_input()
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
    return ip, program, instructions


def get_valid_instructions(change_log, instructions):
    before = change_log['before']
    instruction = change_log['instruction']
    instr_num = instruction[0]
    params = instruction[1:]
    after = change_log['after']
    valid_instructions = [instruction for instruction, fun in instructions.items() if fun(params, before) == after]
    return valid_instructions, instr_num


def part_1():
    # ip_pos, program, instructions = prepare_data()

    # ip = 0
    registry = [0, 0, 0, 0, 0, 0]
    # while ip < len(program):
    #     line = program[ip]
    #     registry[ip_pos] = ip
    #     instr_name, params = line
    #     registry = instructions[instr_name](params, registry)
    #     ip = registry[ip_pos]
    #     ip += 1
    #     print(registry)
    # [1374, 1, 915, 256, 915, 914]
    registry = program_in_python(registry)
    print(registry)


# 0 wrong
# 10551314 wrong
# 42156 too low

def part_2():
    """
    row 0  r[5] = 123
    row 1  r[5] = r[5] & 456
    row 2  r[5] = 1 if r[5] == 72 else 0
    row 3  r[1] = r[5] + r[1]
    row 4  r[1] = 0
    row 5  r[5] = 0
    row 6  r[4] = r[5] | 65536
    row 7  r[5] = 13431073
    row 8  r[3] = r[4] & 255
    row 9  r[5] = r[5] + r[3]
    row 10 r[5] = r[5] & 16777215
    row 11 r[5] = r[5] * 65899
    row 12 r[5] = r[5] & 16777215
    row 13 r[3] = 1 if 256 > r[4] else 0
    row 14 r[1] = r[3] + r[1]
    row 15 r[1] = r[1] + 1
    row 16 r[1] = 27
    row 17 r[3] = 0
    row 18 r[2] = r[3] + 1
    row 19 r[2] = r[2] * 256
    row 20 r[2] = 1 if r[2] > r[4] else 0
    row 21 r[1] = r[2] + r[1]
    row 22 r[1] = r[1] + 1
    row 23 r[1] = 25
    row 24 r[3] = r[3] + 1
    row 25 r[1] = 17
    row 26 r[4] = r[3]
    row 27 r[1] = 7
    row 28 r[3] = 1 if r[5] == r[0] else 0
    row 29 r[1] = r[3] + r[1]
    row 30 r[1] = 5
    """

    """
    init: [?, 0, 0, 0, 0, 0]    # r[0] can be whatever I choose
    row 0  r[5] = 123
    row 1  r[5] = r[5] & 456
    row 2  r[5] = 1 if r[5] == 72 else 0
    row 3  r[1] = r[5] + r[1]
    row 4  r[1] = 0
    row 5  r[5] = 0
    row 6  r[4] = r[5] | 65536
    row 7  r[5] = 13431073
    row 8  r[3] = r[4] & 255
    row 9  r[5] = r[5] + r[3]
    row 10 r[5] = r[5] & 16777215
    row 11 r[5] = r[5] * 65899
    row 12 r[5] = r[5] & 16777215
    row 13 r[3] = 1 if 256 > r[4] else 0
    row 14 r[1] = r[3] + r[1]
    row 15 r[1] = r[1] + 1
    row 16 r[1] = 27
    row 17 r[3] = 0
    row 18 r[2] = r[3] + 1
    row 19 r[2] = r[2] * 256
    row 20 r[2] = 1 if r[2] > r[4] else 0
    row 21 r[1] = r[2] + r[1]
    row 22 r[1] = r[1] + 1
    row 23 r[1] = 25
    row 24 r[3] = r[3] + 1
    row 25 r[1] = 17
    row 26 r[4] = r[3]
    row 27 r[1] = 7
    row 28 r[3] = 1 if r[5] == r[0] else 0
    row 29 r[1] = r[3] + r[1]
    row 30 r[1] = 5
    """

    ip_pos, program, instructions = prepare_data()

    # ip = 0
    registry = [1, 0, 0, 0, 0, 0]
    # count = 0
    # ips = [ip]
    # reg0s = [0]
    # while ip < len(program):
    #     line = program[ip]
    #     registry[ip_pos] = ip
    #     instr_name, params = line
    #     registry = instructions[instr_name](params, registry)
    #     ip = registry[ip_pos]
    #     ip += 1
    #     count += 1
    #     # ips.append(ip)
    #     # reg0s.append(registry[0])
    #     if count % 10000000 == 0:
    #         print(registry)
    #     # if count > 1000:
    #     #     break

    # import numpy as np
    # import matplotlib.pyplot as plt
    # plt.plot(np.arange(0, len(ips), 1), ips)
    # plt.show()
    # plt.plot(np.arange(0, len(reg0s), 1), reg0s)
    # # plt.plot(np.arange(0, len(values) - 1, 1), np.diff(diff_sums))
    # plt.show()

    registry = program_in_python(registry)

    print(registry)


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)