from pdf2image import convert_from_path, convert_from_bytes
from .page import Page
from ..image import Image
from typing import List
import numpy as np

class Document:
    def __init__(self) -> None:
        self.pages: List[Page] = []


    def set_from_path(self, path_file):
        images = convert_from_path(path_file)
        
        for im in images:
            image = Image(img=np.array(im))
            page = Page(image=image)
            self.pages.append(page)