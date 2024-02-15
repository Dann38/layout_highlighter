from abc import ABC
from ..image import ImageSegment
from ..word import Word
from typing import List

class Paragraph(ABC):
    def __init__(self):
        self.segment: ImageSegment
        self.words: List[Word] = []