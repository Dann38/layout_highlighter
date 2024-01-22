from typing import Dict
from ..image.image_segment import ImageSegment


class Word:
    def __init__(self, x0: int = 0, y0: int = 0, x1: int = 0, y1: int = 0, text: str = "", bold: float = None):
        self.segment = ImageSegment(x0, y0, x1, y1)
        self.text = text
        self.bold = bold

    def set_two_points(self, points: Dict):
        """
        x_top_left, y_top_left, x_bottom_right, y_bottom_right
        """
        self.segment.set_segment_2p(points)

    def set_point_and_size(self, point_and_size: Dict):
        """
        x_top_left, y_top_left, width, height
        """
        self.segment.set_segment_p_size(point_and_size)

    def set_text(self, text: str):
        self.text = text

    def set_bold(self, bold: float):
        self.bold = bold

    def to_dict(self) -> Dict:
        any_date = {
            "text": self.text
        }
        any_date["bold"] = round(self.bold, 4) 
        segment = self.segment.get_segment_2p()
        dict_word = dict(list(segment.items()) + list(any_date.items()))
        return dict_word
