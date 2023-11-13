from pydantic import BaseModel
from typing import List, Dict


class CreatePointBboxes(BaseModel):
    list_bboxes: List[Dict]
    count: int


class Point(BaseModel):
    list_point: List[Dict]


class CreateGraph(BaseModel):
    list_point: List[Dict]


class Graph(BaseModel):
    list_edge: List[Dict]


class CreateGraphSegments(BaseModel):
    list_edge: List[Dict]
    list_point: List[Dict]
    threshold: float


class GraphSegment(BaseModel):
    list_edge: List[Dict]
    list_index_point: List[int]
    x_left: int
    y_top: int
    x_right: int
    y_bottom: int
