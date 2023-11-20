from pydantic import BaseModel
from typing import List, Dict


class CreatePointBboxes(BaseModel):
    list_bboxes: List[Dict]
    count: int


class Point(BaseModel):
    list_point: List[Dict]
    bboxes_edge: List[Dict]


class CreateGraph(BaseModel):
    list_point: List[Dict]


class Graph(BaseModel):
    list_edge: List[Dict]


class CreateGraphSegmentsWidth(BaseModel):
    list_edge: List[Dict]
    list_point: List[Dict]
    mandatory_links: List[Dict]
    threshold: float


class CreateGraphSegmentsManual(BaseModel):
    list_edge: List[Dict]
    list_point: List[Dict]
    mandatory_links: List[Dict]
    delete_edges: List[int]


class GraphSegment(BaseModel):
    list_edge: List[Dict]
    list_index_point: List[int]