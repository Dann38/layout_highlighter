from graph.related_graph import RelatedGraph


class Segment:
    def __init__(self, r: RelatedGraph):
        self.list_edge = [{"node1":  edge.get_nodes()[0].index-1, "node2": edge.get_nodes()[1].index-1}
                     for edge in r.get_edges()]
        nodes = r.get_nodes()
        self.list_index_point = [node.index-1 for node in nodes]
        x_array = [node.x for node in nodes]
        y_array = [node.y for node in nodes]
        self.x_left = round(min(x_array))
        self.y_top = round(min(y_array))
        self.x_right = round(max(x_array))
        self.y_bottom = round(max(y_array))

