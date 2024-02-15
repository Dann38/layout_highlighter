from abc import ABC, abstractclassmethod
from img_doc.data_structures import ImageSegment, Word
from typing import List

class BaseBoldWordExtractor(ABC):
    @abstractclassmethod
    def extract(words: List[Word]) -> None:
        pass