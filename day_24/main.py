import functools
import re
from collections import OrderedDict
from enum import Enum
from math import floor

import numpy as np


class Side(Enum):
    IMMUNE_SYSTEM = 'Immune System'
    INFECTION = 'Infection'


class Group(object):

    def __init__(self, side, number, units, hp, immunities, weaknesses, attack_type, attack, initiative):
        self.side = side
        self.number = number
        self.units = units
        self.hp = hp
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.attack_type = attack_type
        self.attack = attack
        self.initiative = initiative

    def __repr__(self) -> str:
        return '{} {}: {} units, {} hp (weak to {}; immune to {}) with attack: {} {} damage, initiative {}'.format(
            self.side.name, self.number, self.units, self.hp, self.weaknesses, self.immunities, self.attack_type,
            self.attack, self.initiative)

    def __hash__(self) -> int:
        return hash(self.side) + hash(self.number) + hash(self.initiative)  # this should be unique per group

    def __eq__(self, o: object) -> bool:
        return hash(self) == hash(o)

    def effective_power(self):
        return self.units * self.attack

    def calc_damage_deal(self, enemy: 'Group'):
        if self.attack_type in enemy.immunities:
            return 0
        if self.attack_type in enemy.weaknesses:
            return self.effective_power() * 2
        return self.effective_power()

    def be_attacked(self, enemy: 'Group'):
        attack_power = enemy.calc_damage_deal(self)
        units_died = min(floor(attack_power / self.hp), self.units)
        self.units -= units_died
        return units_died

    def is_dead(self):
        return self.units <= 0

    def name(self):
        return '{} {}'.format(self.side.name, self.number)

    def is_enemy(self, enemy: 'Group'):
        return self.side != enemy.side


def load_input():
    # groups = []
    groups = set()
    curr_side = None
    i = 0
    with open('input.txt', encoding='utf-8') as lines:
        for line in lines:
            line = line.replace('\n', '')
            if line == '':
                continue
            if line.endswith(':'):
                curr_side = Side(line[:-1])
                i = 0
            else:
                i += 1
                m = re.match(
                    '(\d+) units each with (\d+) hit points (\(.*\) )?with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)',
                    line)
                units = int(m.group(1))
                hp = int(m.group(2))
                properties = m.group(3)
                attack = int(m.group(4))
                attack_type = m.group(5)
                initiative = int(m.group(6))
                weaknesses = []
                immunities = []
                if properties is not None:
                    properties = properties[1:-2].split('; ')
                    for prop in properties:
                        m = re.match('((immune|weak) to )?([a-z, ]+)', prop)
                        types = m.group(3).split(', ')
                        if m.group(2) == 'immune':
                            immunities = types
                        if m.group(2) == 'weak':
                            weaknesses = types
                # groups.append(Group(curr_side, i, units, hp, immunities, weaknesses, attack_type, attack, initiative))
                groups.add(Group(curr_side, i, units, hp, immunities, weaknesses, attack_type, attack, initiative))
    return groups


def target_selection_order_comparison(group_1: Group, group_2: Group):
    effective_power_diff = group_2.effective_power() - group_1.effective_power()
    if effective_power_diff == 0:
        return attack_order_comparison(group_1, group_2)
    return effective_power_diff


def attack_order_comparison(group_1: Group, group_2: Group):
    return group_2.initiative - group_1.initiative


def enemy_selection_order_comparison(group: Group):
    def cmp_func(group_1: Group, group_2: Group):
        taken_damage_diff = group.calc_damage_deal(group_2) - group.calc_damage_deal(group_1)
        if taken_damage_diff == 0:
            effective_power_diff = group_2.effective_power() - group_1.effective_power()
            if effective_power_diff == 0:
                return attack_order_comparison(group_1, group_2)
            return effective_power_diff
        return taken_damage_diff

    return cmp_func


def tick(groups):
    # target selection part
    free_targets = set(groups)
    attack_plan = dict()
    for group in sorted(groups, key=functools.cmp_to_key(target_selection_order_comparison)):
        enemies = sorted(filter(lambda x: x.is_enemy(group), free_targets),
                         key=functools.cmp_to_key(enemy_selection_order_comparison(group)))
        if len(enemies) > 0:
            enemy = enemies[0]
            free_targets.remove(enemy)
        else:
            enemy = None
        attack_plan[group] = enemy

    print(attack_plan)
    # attacking part
    for group in sorted(groups, key=functools.cmp_to_key(attack_order_comparison)):
        defender = attack_plan[group]
        if defender is None:
            continue
        units_killed = defender.be_attacked(group)
        print('{} attacks {}, killing {} units'.format(group.name(), defender.name(), units_killed))
        if defender.is_dead():
            groups.remove(defender)
    return groups

# 21046 too low
def part_1():
    groups = load_input()
    someone_wins = False
    survived_units = dict()
    while not someone_wins:
        groups = tick(groups)
        for side in Side:
            side_groups = list(filter(lambda x: x.side == side, groups))
            survived_units[side] = sum([g.units for g in side_groups])
            if len(side_groups) == 0:
                someone_wins = True

    print(max(survived_units.values()))


def part_2():
    pass


if __name__ == '__main__':
    from time import time

    start = time()

    part_1()
    part_2()

    print(time() - start)
