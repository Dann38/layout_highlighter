from fastapi import FastAPI

import uvicorn
import schemas
from typing import List
from graph.delone_binder import DeloneBinder, Node, Edge
from graph.graph import Graph
from graph.segment import Segment

app = FastAPI()


def run_api(host: str, port: int) -> None:
    uvicorn.run(app=app, host=host, port=port)


@app.post("/bboxes_to_points/")
async def bboxes_to_points(bboxes: schemas.CreatePointBboxes) -> schemas.Point:
    points_list = []
    if bboxes.count == 1:
        for bbox in bboxes.list_bboxes:
            y = round(bbox["y_top_left"] + bbox["height"] / 2)
            x = round(bbox["x_top_left"] + bbox["width"] / 2)
            points_list.append({"x": x, "y": y})
    return schemas.Point(list_point=points_list)


@app.post("/point_to_delone/")
async def point_to_delone(points: schemas.CreateGraph) -> schemas.Graph:
    delone_binder = DeloneBinder()
    nodes = [Node(point["x"], point["y"]) for point in points.list_point]
    dict_nodes = dict()
    for i, node in enumerate(nodes):
        dict_nodes[node] = i
    edges, triangle = delone_binder.bind(nodes)
    edges_result = [{"node1": dict_nodes[edge.node1], "node2": dict_nodes[edge.node2], "width": edge.width} for edge in edges]
    return schemas.Graph(list_edge=edges_result)


@app.post("/delone_to_graph_segments/")
async def point_to_delone(related_graph: schemas.CreateGraphSegments) -> List[schemas.GraphSegment]:
    graph = Graph()
    for i, point in enumerate(related_graph.list_point):
        graph.add_node(point["x"], point["y"])

    new_edge = [edge for edge in related_graph.list_edge if edge["width"] < related_graph.threshold]

    for edge in new_edge:
        graph.add_edge(edge["node1"] + 1, edge["node2"] + 1)

    segments = [Segment(r) for r in graph.get_related_graphs()]
    return [schemas.CreateGraphSegments(
        list_edge=seg.list_edge,
        list_index_point=seg.list_index_point,
        x_left=seg.x_left,
        y_top=seg.y_top,
        x_right=seg.x_right,
        y_bottom=seg.y_bottom
        ) for seg in segments]
