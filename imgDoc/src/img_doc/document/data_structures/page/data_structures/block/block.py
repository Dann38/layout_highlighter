from abc import ABC
from typing import List
from ..paragraph import Paragraph
from ..image import ImageSegment
from ..word import Word

LABEL = ["no_struct", "text", "header",  "list", "table"]

class Block(ABC):
    def __init__(self):
        self.paragraphs: List[Paragraph] = []
        self.segment: ImageSegment
        self.words: List[Word] = []
        self.label: int
    
