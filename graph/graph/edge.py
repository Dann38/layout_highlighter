from .node import Node
from typing import Tuple, List, Set


class Edge:
    def __init__(self, nodes: Set[Node]):
        self.nodes = nodes

    def get_line(self) -> Tuple[List[float], List[float]]:
        x = []
        y = []
        for node in self.nodes:
            x.append(node.x)
            y.append(node.y)

        return x, y

    def get_nodes(self) -> List[Node]:
        return list(self.nodes)
