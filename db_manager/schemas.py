from pydantic import BaseModel
from typing import List, Tuple


class ImageBase(BaseModel):
    bytes_img: bytes


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: str
    bytes_img: bytes


class ProcessingBase(BaseModel):
    id_image: str


class ProcessingCreate(ProcessingBase):
    pass


class Processing(ProcessingBase):
    id: str


class LabelCreate(BaseModel):
    name: str


class Label(BaseModel):
    id: int
    name: str


class SegmentCreate(BaseModel):
    id_image: str
    x0: int
    x1: int
    y0: int
    y1: int
    id_label: int
    nodes: List[Tuple[int, int]]
    edges: List[Tuple[int, int]]


class Segment(SegmentCreate):
    id: str
    image: bytes
