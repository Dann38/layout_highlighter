from pydantic import BaseModel
from typing import List, Tuple


# class ImageBase(BaseModel):
#     bytes_img: bytes


# class ImageCreate(ImageBase):
#     pass


# class Image(ImageBase):
#     id: str
#     bytes_img: bytes


# class ProcessingBase(BaseModel):
#     id_image: str


# class ProcessingCreate(ProcessingBase):
#     pass


# class Processing(ProcessingBase):
#     id: str


# class LabelCreate(BaseModel):
#     name: str


# class Label(BaseModel):
#     id: int
#     name: str


# class SegmentCreate(BaseModel):
#     id_image: str
#     x0: int
#     x1: int
#     y0: int
#     y1: int
#     id_label: int
#     nodes: List[Tuple[int, int]]
#     edges: List[Tuple[int, int]]


# class Segment(SegmentCreate):
#     id: str
#     image: bytes


class BaseDocument(BaseModel):
    name: str
    image64: bytes

class CreateDocument(BaseDocument):
    pass

class Document(BaseDocument):
    id: int

class BaseProcessing(BaseModel):
    name: str
    json_processing: str

class CreateProcessing(BaseProcessing):
    pass

class Processing(BaseProcessing):
    id: int
