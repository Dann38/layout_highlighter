from typing import Dict
from img_doc.image import ImageSegment


class Word:
    def __init__(self, dict_word):
        self.segment = ImageSegment()
        if "width" in dict_word.keys():
            self.set_point_and_size(dict_word)
        else:
            self.set_two_points(dict_word)
        
        self.text = ""
        if "text" in dict_word.keys():
            self.set_text(dict_word["text"])
        
        self.bold = None
        if "bold" in dict_word.keys():
            self.set_bold(dict_word["bold"])
        
        

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
        if self.bold is not None:
            any_date["bold"] = round(self.bold, 4) 
        segment = self.segment.get_segment_2p()
        dict_word = dict(list(segment.items()) + list(any_date.items()))
        return dict_word
