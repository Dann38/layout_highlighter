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
    bboxes_edge = []
    index = 0
    if bboxes.count == 1:
        for i, bbox in enumerate(bboxes.list_bboxes):
            y = round(bbox["y_top_left"] + bbox["height"] / 2)
            x = round(bbox["x_top_left"] + bbox["width"] / 2)
            points_list.append({"x": x, "y": y})

    elif bboxes.count == 2:
        for i, bbox in enumerate(bboxes.list_bboxes):
            y = round(bbox["y_top_left"] + bbox["height"] / 2)
            x1 = bbox["x_top_left"]
            x2 = bbox["x_top_left"] + bbox["width"]
            points_list.append({"x": x1, "y": y})
            points_list.append({"x": x2, "y": y})
            index += 2
            bboxes_edge.append({"node1": index-2, "node2": index-1})

    elif bboxes.count == 3:
        for i, bbox in enumerate(bboxes.list_bboxes):
            y = round(bbox["y_top_left"] + bbox["height"] / 2)
            x0 = bbox["x_top_left"]
            x1 = round(bbox["x_top_left"] + bbox["width"] / 2)
            x2 = bbox["x_top_left"] + bbox["width"]
            points_list.append({"x": x0, "y": y})
            points_list.append({"x": x1, "y": y})
            points_list.append({"x": x2, "y": y})
            index += 3
            bboxes_edge.append({"node1": index - 3, "node2": index - 2})
            bboxes_edge.append({"node1": index - 2, "node2": index - 1})

    return schemas.Point(list_point=points_list, bboxes_edge=bboxes_edge)


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


@app.post("/width_segments/")
async def width_segments(related_graph: schemas.CreateGraphSegmentsWidth) -> List[schemas.GraphSegment]:
    graph = Graph()
    index_and_id_node = dict()
    id_list = []
    for i, point in enumerate(related_graph.list_point):
        id_ = graph.add_node(point["x"], point["y"])
        index_and_id_node[id_] = i
        id_list.append(id_)

    new_edge = [edge for edge in related_graph.list_edge
                if edge["width"] < related_graph.threshold] + related_graph.mandatory_links

    for edge in new_edge:
        graph.add_edge(id_list[edge["node1"]], id_list[edge["node2"]])

    segments = [Segment(r, index_and_id_node) for r in graph.get_related_graphs()]
    return [schemas.GraphSegment(
        list_edge=seg.list_edge,
        list_index_point=seg.list_index_point,
        ) for seg in segments]


@app.post("/manual_segments/")
async def manual_segments(related_graph: schemas.CreateGraphSegmentsManual) -> List[schemas.GraphSegment]:
    graph = Graph()
    index_and_id_node = dict()
    id_list = []
    for i, point in enumerate(related_graph.list_point):
        id_ = graph.add_node(point["x"], point["y"])
        index_and_id_node[id_] = i
        id_list.append(id_)

    new_edge = [edge for i, edge in enumerate(related_graph.list_edge)
                if not (i in related_graph.delete_edges)] + related_graph.mandatory_links

    for edge in new_edge:
        graph.add_edge(id_list[edge["node1"]], id_list[edge["node2"]])

    segments = [Segment(r, index_and_id_node) for r in graph.get_related_graphs()]
    return [schemas.GraphSegment(
        list_edge=seg.list_edge,
        list_index_point=seg.list_index_point,
        ) for seg in segments]
