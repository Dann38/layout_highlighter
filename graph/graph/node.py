from typing import Set


class Node:
    def __init__(self, x: float, y: float, index: int):
        self.x = x
        self.y = y
        self.index = index
        self.neighbors = []

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

    def add_neighbor(self, node: "Node"):
        self.neighbors.append(node)

    def get_neighbors(self) -> Set["Node"]:
        return set(self.neighbors)


class NoneNode(Node):
    def __init__(self):
        super(NoneNode, self).__init__(0, 0, 0)
        self.x = None
        self.y = None
        self.index = None

