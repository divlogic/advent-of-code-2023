import re
from pathlib import Path
from typing import Dict


class Node:
    def __init__(self, desc: str) -> None:
        point_pattern = r"^\w{3}"
        point = re.match(point_pattern, desc).group()
        tuple_pattern = r"\((\w{3}), (\w{3})\)"
        options = re.search(tuple_pattern, desc)
        options = (options.group(1), options.group(2))
        self.point = point
        self.options = options

    def left(self) -> str:
        return self.options[0]

    def right(self) -> str:
        return self.options[1]


class NodeNetwork:
    def __init__(self, path: str, start: str, nodes: Dict[str, Node]) -> None:
        self.path = path
        self.position = 0
        self.steps = 0
        self.nodes = nodes
        self.current = start

    def next(self):
        if self.path[self.position] == "L":
            self.current = self.nodes[self.current].left()
        elif self.path[self.position] == "R":
            self.current = self.nodes[self.current].right()
        if len(self.path) == self.position + 1:
            self.position = 0
        else:
            self.position += 1
        self.steps += 1


def find_answer(filename) -> int:
    with open(Path(__file__).parents[1] / (filename)) as file:
        lines = file.readlines()
    path = re.match("[RL]+", lines[0]).group(0)
    nodes = {}
    for line in lines[2:]:
        node = Node(line)
        nodes[node.point] = node
    node_network = NodeNetwork(path, "AAA", nodes)

    count = 0

    while node_network.current != "ZZZ" and count < 100000:
        node_network.next()
        count += 1
    if count == 10000:
        raise (Exception("Hit the count limit"))
    answer = node_network.steps
    return answer
