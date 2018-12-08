import numpy as np


class Node(object):

    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    @staticmethod
    def parse_part(numbers):
        children_len = numbers[0]
        metadata_len = numbers[1]
        children = []
        numbers = numbers[2:]
        for i in range(children_len):
            child, numbers = Node.parse_part(numbers)
            children.append(child)
        metadata = numbers[:metadata_len]
        return Node(children, metadata), numbers[metadata_len:]

    def get_entries_sum(self):
        return sum(self.metadata) + sum([i.get_entries_sum() for i in self.children])


if __name__ == '__main__':
    with open('input.txt', encoding='utf-8') as lines:
        line = next(lines)
    data = [int(i) for i in line.split(' ')]
    root, _ = Node.parse_part(data)

    print(root.get_entries_sum())
