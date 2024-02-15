# from . import Word, Row
# from .base_info import BaseInfo
# from ..image import ImageSegment
# from typing import List, Dict

# LABEL = {
#     "no_struct": 0,
#     "multiple_blocks": 1,
#     "text": 2,
#     "header": 3,
#     "list": 4,
#     "table": 5,
# }

# INT_LABEL = {
#     0: "no_struct",
#     1: "multiple_blocks",
#     2: "text",
#     3: "header",
#     4: "list",
#     5: "table",
# }
# class Block:
#     def __init__(self, rows: List[Row] = [], words: List[Word] = [], label: int = LABEL["text"], 
#                  info: BaseInfo = None, caption: BaseInfo = None, notes: BaseInfo = None,
#                  x0: int = 0, y0: int = 0, x1: int = 0, y1: int = 0):
#         self.rows = rows
#         self.words = words
#         self.label: int = label
#         self.segment = ImageSegment(x0, y0, x1, y1)

#         self.info = info
#         self.caption = caption
#         self.notes = notes

#     def set_words(self, words):
#         self.words = words
#         self.segment.set_segment_max_segments([word.segment for word in words])


#     def to_dict(self) -> Dict:
#         any_date = {
#             "label_int": self.label,
#             "label": INT_LABEL[self.label]
#         }
#         segment = self.segment.get_segment_2p()
#         dict_block = dict(list(segment.items()) + list(any_date.items()))
#         return dict_block
