from abc import ABC
import numpy as np

from typing import Dict, List


class ImageSegment(ABC):
    def __init__(self, x_top_left, y_top_left, x_bottom_right, y_bottom_right):
        self.x_top_left = x_top_left
        self.y_top_left = y_top_left
        self.x_bottom_right = x_bottom_right
        self.y_bottom_right = y_bottom_right

    def get_segment_from_img(self, img: np.ndarray):
        h0 = self.y_top_left
        h1 = self.y_bottom_right
        w0 = self.x_top_left
        w1 = self.x_bottom_right
        return img[h0:h1, w0:w1, :] if len(img.shape) == 3 else img[h0:h1, w0:w1]

    def get_segment_2p(self):
        return {
            "x_top_left": self.x_top_left,
            "x_bottom_right": self.x_bottom_right,
            "y_top_left": self.y_top_left,
            "y_bottom_right": self.y_bottom_right
        }

    def get_height(self):
        return self.y_bottom_right-self.y_top_left

    def get_width(self):
        return self.x_bottom_right - self.x_top_left

    def get_center(self):
        x_c = round((self.x_top_left + self.x_bottom_right) / 2)
        y_c = round((self.y_top_left + self.y_bottom_right) / 2)
        return x_c, y_c

    def set_segment_2p(self, dict_2point: Dict):
        self.x_top_left = dict_2point["x_top_left"]
        self.y_top_left = dict_2point["y_top_left"]
        self.x_bottom_right = dict_2point["x_bottom_right"]
        self.y_bottom_right = dict_2point["y_bottom_right"]

    def set_segment_p_size(self, dict_2point: Dict):
        self.x_top_left = dict_2point["x_top_left"]
        self.y_top_left = dict_2point["y_top_left"]
        self.x_bottom_right = dict_2point["width"] + self.x_top_left
        self.y_bottom_right = dict_2point["height"] + self.y_top_left

    def set_segment_max_segments(self, segments: List["ImageSegment"]):
        list_x_top_left = [segment.x_top_left for segment in segments]
        list_y_top_left = [segment.y_top_left for segment in segments]
        list_x_bottom_right = [segment.x_bottom_right for segment in segments]
        list_y_bottom_right = [segment.y_bottom_right for segment in segments]
        self.x_top_left = min(list_x_top_left)
        self.y_top_left = min(list_y_top_left)
        self.x_bottom_right = max(list_x_bottom_right)
        self.y_bottom_right = max(list_y_bottom_right)
