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

    def get_value(self):
        if len(self.children) == 0:
            return sum(self.metadata)

        return sum([self.children[metadatum - 1].get_value() for metadatum in self.metadata
                    if metadatum <= len(self.children)])


def part_1():
    with open('input.txt', encoding='utf-8') as lines:
        line = next(lines)
    data = [int(i) for i in line.split(' ')]
    root, _ = Node.parse_part(data)

    print(root.get_entries_sum())


def part_2():
    from time import time
    start = time()
    with open('../day_8_part_1/input.txt', encoding='utf-8') as lines:
        line = next(lines)
    data = [int(i) for i in line.split(' ')]
    root, _ = Node.parse_part(data)

    print(root.get_value())
    print(time() - start)


if __name__ == '__main__':
    part_1()
    part_2()
