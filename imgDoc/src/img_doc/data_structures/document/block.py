from . import Word, Row
from ..image import ImageSegment
from typing import List

class Block:
    def __init__(self, rows: List[Row] = [], words: List[Word] = [],
                 x0: int = 0, y0: int = 0, x1: int = 0, y1: int = 0):
        self.rows = rows
        self.words = words
        self.segment = ImageSegment(x0, y0, x1, y1)

    def set_words(self, words):
        self.words = words
        self.segment.set_segment_max_segments([word.segment for word in words])

    def intersection(self, block):
        seg = block.segment
        points1 = [(seg.x_top_left, seg.y_top_left),
                   (seg.x_top_left, seg.y_bottom_right),
                   (seg.x_bottom_right, seg.y_top_left),
                   (seg.x_bottom_right, seg.y_bottom_right)]

        new_seg = self.segment
        points2 = [(new_seg.x_top_left, new_seg.y_top_left),
                   (new_seg.x_top_left, new_seg.y_bottom_right),
                   (new_seg.x_bottom_right, new_seg.y_top_left),
                   (new_seg.x_bottom_right, new_seg.y_bottom_right)]

        for p in points1:
            if (new_seg.x_top_left < p[0]) and (new_seg.x_bottom_right > p[0]) and \
                    (new_seg.y_top_left < p[1]) and (new_seg.y_bottom_right > p[1]):
                return True
        for p in points2:
            if (seg.x_top_left < p[0]) and (seg.x_bottom_right > p[0]) and \
                    (seg.y_top_left < p[1]) and (seg.y_bottom_right > p[1]):
                return True
        return False

    def add_block_in_block(self, block):
        self.words += block.words
        self.rows += block.rows

        c2 = block.segment.get_segment_2p()

        self.segment.set_segment_2p({
            "x_top_left": min(self.segment.x_top_left, c2["x_top_left"]),
            "x_bottom_right": max(self.segment.x_bottom_right, c2["x_bottom_right"]),
            "y_top_left": min(self.segment.y_top_left, c2["y_top_left"]),
            "y_bottom_right": max(self.segment.y_bottom_right, c2["y_bottom_right"]),
        })
