from typing import List, Tuple

import numpy as np
from scipy.spatial import Delaunay


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Edge:
    def __init__(self, node1: Node, node2: Node):
        self.node1 = node1
        self.node2 = node2
        self.width = self.__get_size()

    def __get_size(self):
        return np.sqrt((self.node1.x - self.node2.x)**2 + (self.node1.y - self.node2.y)**2)

    def get_lines(self) -> Tuple[List[float], List[float]]:
        return [self.node1.x, self.node2.x], [self.node1.y, self.node2.y]


class Triangle:
    def __init__(self, node1, node2, node3):
        self.node1 = node1
        self.node2 = node2
        self.node3 = node3
        self.area = self.__get_area()

    def __get_area(self):
        s_1 = 0
        s_2 = 0
        point_prev = self.node3
        for point in [self.node1, self.node2, self.node3]:
            x, y = point.x, point.y
            x_prev, y_prev = point_prev.x, point_prev.y
            point_prev = point
            s_1 += y * x_prev
            s_2 += x * y_prev

        return abs((s_2 - s_1) / 2)


class DeloneBinder:
    def __init__(self):
        pass

    def bind(self, nodes: List[Node]) -> Tuple[List[Edge], List[Triangle]]:
        points = np.array([(node.x, node.y) for node in nodes])
        delone = Delaunay(points)
        edges = self.__get_edges_from_delone(delone, nodes)
        triangles = self.__get_triangles_from_delone(delone, nodes)
        return edges, triangles

    def __get_edges_from_delone(self, delone: Delaunay, nodes: List[Node]) -> List[Edge]:
        edges = set([])
        for tr in delone.simplices:
            edges.add(frozenset([tr[0], tr[1]]))
            edges.add(frozenset([tr[1], tr[2]]))
            edges.add(frozenset([tr[2], tr[0]]))

        edges = [list(edge) for edge in list(edges)]
        edges = [Edge(nodes[edge[0]], nodes[edge[1]]) for edge in edges]
        return edges

    def __get_triangles_from_delone(self, delone: Delaunay, nodes: List[Node]) -> List[Triangle]:
        triangles = []
        for tr in delone.simplices:
            triangles.append(Triangle(nodes[tr[0]], nodes[tr[1]], nodes[tr[2]]))
        return triangles
