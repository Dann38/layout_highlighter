from pydantic import BaseModel
from typing import List, Tuple


class BaseDocument(BaseModel):
    name: str
    image64: bytes


class CreateDocument(BaseDocument):
    folder_parent_id: int = 0


class Document(BaseDocument):
    id: int

# -------------------------------------------------
    
class BaseProcessing(BaseModel):
    name: str
    json_processing: str


class CreateProcessing(BaseProcessing):
    pass


class Processing(BaseProcessing):
    id: int

# -------------------------------------------------

class BaseDataset(BaseModel):
    name: str
    discription: str


class CreateDataset(BaseDataset):
    pass


class Dataset(BaseDataset):
    id: int

# -------------------------------------------------
  
class BaseMarkingSegment(BaseModel):
    name: str
    dataset_id: int


class CreateMarkingSegment(BaseMarkingSegment):
    pass


class MarkingSegment(BaseMarkingSegment):
    id: int

 # ------------------------------------------------- 

class BaseSegmentData(BaseModel):
    json_data: str
    document_id: int
    marking_id: int


class CreateSegmentData(BaseSegmentData):
    pass


class SegmentData(BaseSegmentData):
    id: int


#
    
class DatasetAll(BaseModel):
    documents: List[Document]
    segments: List[SegmentData]
    marking: List[MarkingSegment]

class BaseFolder(BaseModel):
    name: str

class CreateFolder(BaseFolder):
    folder_parent_id: int = 0

class Folder(BaseFolder):
    id: int
    folders_id: List[int]
    documents_id: List[int]