from abc import ABC
import numpy as np
from .image_segment import ImageSegment
import os
import cv2
import base64


class Image(ABC):
    """
    img : RGB !!!
    name: text.format
    """
    def __init__(self, img: np.ndarray = np.zeros((10,10)), name_image: str = "None"):
        self.img = img
        self.segment = ImageSegment(0, 0, self.img.shape[1], self.img.shape[0])
        self.name_img = name_image

    def set_img_from_path(self, path):
        self.name_img = os.path.basename(path)
        self.img = self.__read(path)
        self.segment = ImageSegment(0, 0, self.img.shape[1], self.img.shape[0])

    def get_base64(self):
        img_type = "jpg" if self.name_img == "None" else self.name_img.split(".")[-1]
        _, img_array = cv2.imencode(f'.{img_type}', self.img)
        img_bytes = img_array.tobytes()
        return base64.b64encode(img_bytes)

    def __read(self, path):
        with open(path, "rb") as f:
            chunk = f.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        return cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)

