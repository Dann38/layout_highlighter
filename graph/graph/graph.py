from .related_graph import RelatedGraph
from .edge import Edge
from .node import Node
from typing import List, Dict, Tuple, Set


class Graph:
    def __init__(self):
        self.related_graphs: Set[RelatedGraph] = set()
        self.nodes: Dict[int, Node] = dict()
        self.nodes_in_graphs: Dict[int, RelatedGraph] = dict()
        self.id_cursor = 0

    def get_edges(self) -> List[Edge]:
        return [edge for r in self.related_graphs for edge in r.get_edges()]

    def get_nodes(self) -> List[Node]:
        return [node for r in self.related_graphs for node in r.get_nodes()]

    def get_node(self, index) -> Node:
        return self.nodes[index]

    def get_related_graphs(self) -> List[RelatedGraph]:
        return list(self.related_graphs)

    def get_related_graph_from_index_node(self, index_node: int) -> RelatedGraph:
        return self.nodes_in_graphs[index_node]

    def add_node(self, x: float, y: float) -> int:
        self.id_cursor += 1
        node = Node(x, y, self.id_cursor)
        self.nodes[self.id_cursor] = node

        r = RelatedGraph(node)
        self.nodes_in_graphs[self.id_cursor] = r
        self.related_graphs.add(r)

        return self.id_cursor

    def add_edge(self, index_node1: int, index_node2):
        n1, r1 = self._get_couple_node_related_graph(index_node1)
        n2, r2 = self._get_couple_node_related_graph(index_node2)

        if r1 == r2:
            r1.add_edge(n1, n2)
        else:
            self.related_graphs.remove(r2)
            r1.add_related_graph(this_node=n1, other_related_graph=r2, other_node=n2)
            keys = [key for key, node in self.nodes.items() if node in r1.get_nodes()]
            for key in keys:
                self.nodes_in_graphs[key] = r1


    def delete_edge(self, index_node1, index_node2):
        n1 = self.get_node(index_node1)
        n2 = self.get_node(index_node2)
        r = self.get_related_graph_from_index_node(index_node1)
        new_r = r.delete_edge_from_nodes(n1, n2)
        if len(new_r) == 2:
            self.related_graphs.remove(r)
            self.related_graphs.add(new_r[0])
            self.related_graphs.add(new_r[1])
            for index in [0, 1]:
                keys = [key for key, node in self.nodes.items() if node in new_r[index].get_nodes()]
                for key in keys:
                    self.nodes_in_graphs[key] = new_r[index]

    def _get_couple_node_related_graph(self, index) -> Tuple[Node, RelatedGraph]:
        return self.get_node(index), self.nodes_in_graphs[index]
