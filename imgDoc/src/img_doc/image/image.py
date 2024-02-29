from abc import ABC
import numpy as np
from .image_segment import ImageSegment
import os
import cv2
import base64
import matplotlib.pyplot as plt 

from .editors.binarizer import ValleyEmphasisBinarizer

BINARIZER = {
    "valley_emphasis": ValleyEmphasisBinarizer()
}

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

    def set_base64(self, image64):
        data = np.frombuffer(base64.b64decode(image64), np.uint8)
        image_np = cv2.imdecode(data, cv2.IMREAD_COLOR)
        self.img=image_np
        return

    def __read(self, path):
        with open(path, "rb") as f:
            chunk = f.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        return cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)


    def plot(self):
        plt.imshow(self.img)

    def resize(self, k):
        dim = (round(k*self.img.shape[1]), round(k*self.img.shape[0]))
        self.img = cv2.resize(self.img, dim, interpolation = cv2.INTER_AREA)
        self.segment.resize(k)

    def get_binary_image(self, method:str = "valley_emphasis", conf={}):
        return BINARIZER[method].binarize(self.img)
