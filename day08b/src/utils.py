import math
import re
from pathlib import Path
from typing import Dict, List


class Node:
    def __init__(self, desc: str) -> None:
        point_pattern = r"^\w{3}"
        point = re.match(point_pattern, desc).group()
        tuple_pattern = r"\((\w{3}), (\w{3})\)"
        options = re.search(tuple_pattern, desc)
        options = (options.group(1), options.group(2))
        self.point = point
        self.options = options
        self.touched = False

    def left(self) -> str:
        return self.options[0]

    def right(self) -> str:
        return self.options[1]

    def __str__(self) -> str:
        return f"{self.point} = {self.options} touched: {self.touched}"


class NodeWalker:
    def __init__(self, path: str, start: str, nodes: Dict[str, Node]) -> None:
        self.path = path
        self.position = 0
        self.steps = 0
        self.nodes = nodes
        self.current = start
        self.starting_point = start
        self.steps_since_last = 0
        self.intervals = []

    def next(self):
        self.nodes[self.current].touched = True
        if self.path[self.position] == "L":
            self.current = self.nodes[self.current].left()
        elif self.path[self.position] == "R":
            self.current = self.nodes[self.current].right()

        self.steps_since_last += 1
        if self.current[-1] == "Z":
            self.intervals.append(self.steps_since_last)
            self.steps_since_last = 0

        if len(self.path) == self.position + 1:
            self.position = 0
        else:
            self.position += 1
        self.steps += 1


class Group:
    def __init__(self, networks: List[NodeWalker]) -> None:
        self.container = networks

    def arrived(self) -> bool:
        ending_characters = ""
        for network in self.container:
            ending_characters += network.current[-1]

        return ending_characters.count("Z") == len(ending_characters)


def find_answer(filename) -> int:
    with open(Path(__file__).parents[1] / (filename)) as file:
        lines = file.readlines()
    path = re.match("[RL]+", lines[0]).group(0)
    nodes = {}
    starting_points = []
    for line in lines[2:]:
        node = Node(line)
        nodes[node.point] = node
        if node.point[-1] == "A":
            starting_points.append(node.point)

    node_networks = []

    for item in starting_points:
        node_networks.append(NodeWalker(path, item, nodes))

    group = Group(node_networks)

    count = 0

    while group.arrived() is not True and count < 100000:
        for item in group.container:
            item.next()

        count += 1
    answer = math.lcm(*[item.intervals[0] for item in group.container])

    return answer
