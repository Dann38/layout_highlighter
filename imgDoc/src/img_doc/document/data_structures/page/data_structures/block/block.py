from abc import ABC
from typing import List
from ..paragraph import Paragraph
from ..image import ImageSegment
from ..word import Word

BLOCK_LABEL = ["no_struct", "text", "header",  "list", "table"]

class Block(ABC):
    def __init__(self):
        self.paragraphs: List[Paragraph] = []
        self.segment: ImageSegment
        self.words: List[Word] = []
        self.label: int
    

    def extract_place_in_block_word_segments(self):
        block_h = self.segment.get_height()
        block_w = self.segment.get_width()
        block_dict = self.segment.get_segment_2p()
        x0, y0 = block_dict["x_top_left"],block_dict["y_top_left"] 
        for word in self.words:
            word_dict = word.segment.get_segment_2p()
            x1, y1 = word_dict["x_top_left"],word_dict["y_top_left"]
            word.segment.add_info("place_in_block",((x1-x0)/block_w, (y1-y0)/block_h))