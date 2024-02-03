from . import Word, Row
from .base_info import BaseInfo
from ..image import ImageSegment
from typing import List, Dict

LABEL = {
    "no_struct": 0,
    "multiple_blocks": 1,
    "text": 2,
    "header": 3,
    "list": 4,
    "table": 5,
}

INT_LABEL = {
    0: "no_struct",
    1: "multiple_blocks",
    2: "text",
    3: "header",
    4: "list",
    5: "table",
}
class Block:
    def __init__(self, rows: List[Row] = [], words: List[Word] = [], label: int = LABEL["text"], 
                 info: BaseInfo = None, caption: BaseInfo = None, notes: BaseInfo = None,
                 x0: int = 0, y0: int = 0, x1: int = 0, y1: int = 0):
        self.rows = rows
        self.words = words
        self.label: int = label
        self.segment = ImageSegment(x0, y0, x1, y1)

        self.info = info
        self.caption = caption
        self.notes = notes

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

    def to_dict(self) -> Dict:
        any_date = {
            "label_int": self.label,
            "label": INT_LABEL[self.label]
        }
        segment = self.segment.get_segment_2p()
        dict_block = dict(list(segment.items()) + list(any_date.items()))
        return dict_block
