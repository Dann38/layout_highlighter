from graph.related_graph import RelatedGraph
from typing import List


class Segment:
    def __init__(self, r: RelatedGraph, index_and_id_node: dict):
        self.list_edge = [{"node1": index_and_id_node[edge.get_nodes()[0].index],
                           "node2": index_and_id_node[edge.get_nodes()[1].index]}
                          for edge in r.get_edges()]
        nodes = r.get_nodes()
        self.list_index_point = [index_and_id_node[node.index] for node in nodes]


