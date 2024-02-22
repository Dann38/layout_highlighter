from abc import ABC, abstractclassmethod
from img_doc.document.page import Word
from img_doc.image import ImageSegment
from typing import List

class BaseBoldWordExtractor(ABC):
    @abstractclassmethod
    def extract(words: List[Word]) -> None:
        pass