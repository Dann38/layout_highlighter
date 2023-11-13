from .node import Node, NoneNode
from .edge import Edge

from typing import List


class RelatedGraph:
    def __init__(self, node: Node):
        self.nodes = {node: node.index}
        self.edges = dict()

    def get_nodes(self) -> List[Node]:
        return list(self.nodes.keys())

    def add_node(self, node: Node, node_connect: Node):
        if not (node_connect in self.nodes):
            print("НЕТ УЗЛА ДЛЯ СОЕДИНЕНИЯ")
            return
        if not (node in self.nodes):
            self.nodes[node] = node.index
        self.add_edge(node, node_connect)

    def add_edge(self, node1: Node, node2: Node):
        if not (node1 in self.nodes) or not (node2 in self.nodes):
            print("НЕТ ТАКИХ УЗЛОВ")
            return
        keys_edge = tuple({self.nodes[node1], self.nodes[node2]})
        if keys_edge in self.edges:
            print("УЗЕЛ УЖЕ ЕСТЬ")
        self.edges[keys_edge] = Edge({node1, node2})
        node1.add_neighbor(node2)
        node2.add_neighbor(node1)

    def get_edges(self) -> List[Edge]:
        return [edge for key_edge, edge in self.edges.items()]

    def get_edge_from_nodes(self, node1: Node, node2: Node) -> Edge:
        key_edge = tuple({self.nodes[node1], self.nodes[node2]})
        return self.edges[key_edge]

    def delete_edge(self, edge: Edge):
        node1, node2 = edge.get_nodes()
        self.delete_edge_from_nodes(node1, node2)

    def delete_edge_from_nodes(self, node1: Node, node2: Node) -> List["RelatedGraph"]:
        key_edge = tuple({self.nodes[node1], self.nodes[node2]})
        self.edges.pop(key_edge)

        node1.neighbors.remove(node2)
        node2.neighbors.remove(node1)

        neighbors_node1 = node1.get_neighbors()
        neighbors_node2 = node2.get_neighbors()

        graph1_nodes = []
        graph1_edges_key = set()
        sub_set = neighbors_node1.intersection(neighbors_node2)
        if len(sub_set) > 0:
            return [self]

        nodes = neighbors_node1 - sub_set

        while len(nodes) != 0:
            node = nodes.pop()
            if not (node in graph1_nodes):
                graph1_nodes.append(node)
            if node == node2:
                return [self]
            nodes_new = node.get_neighbors()
            for node_new in nodes_new:
                keys_edge_new = tuple({self.nodes[node_new], self.nodes[node]})
                graph1_edges_key.add(keys_edge_new)
            nodes.union(nodes_new)

        graph2_edges_key = set(self.edges.keys()) - graph1_edges_key
        graph1 = self.create_related_graph(graph1_edges_key)
        graph2 = self.create_related_graph(graph2_edges_key)
        return [graph1, graph2]

    def create_related_graph(self, edges_key) -> "RelatedGraph":
        none_node = NoneNode()
        r = RelatedGraph(none_node)

        for key in edges_key:
            r.edges[key] = self.edges[key]

        nodes = set()
        for key in edges_key:
            n1, n2 = self.edges[key].get_nodes()
            nodes.add(n1)
            nodes.add(n2)

        for node in nodes:
            r.nodes[node] = node.index

        r.nodes.pop(none_node)
        return r

    def add_related_graph(self, other_related_graph: "RelatedGraph", this_node: Node, other_node):
        for node in other_related_graph.get_nodes():
            self.nodes[node] = node.index

        for key, edge in other_related_graph.edges.items():
            self.edges[key] = edge

        self.add_edge(other_node, this_node)
