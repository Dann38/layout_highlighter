from pydantic import BaseModel
from typing import List, Dict


class CreatePointBboxes(BaseModel):
    list_bboxes: List[Dict]
    count: int


class Point(BaseModel):
    list_point: List[Dict]
