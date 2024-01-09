from .word import Word
from ..image.image_segment import ImageSegment
from typing import List


class Row:
    def __init__(self, words: List[Word], x0: int = 0, y0: int = 0, x1: int = 0, y1: int = 0):
        self.words: List[Word] = words
        self.segment = ImageSegment(x0, y0, x1, y1)
        self.segment.set_segment_max_segments([word.segment for word in words])

    def set_words(self, words: List[Word]):
        self.words = words
        self.segment.set_segment_max_segments([word.segment for word in words])