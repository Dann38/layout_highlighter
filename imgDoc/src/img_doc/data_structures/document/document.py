from pdf2image import convert_from_path, convert_from_bytes
from .page import Page
from .templayte import Templayte
from ..image import Image
from typing import List
import numpy as np

IMAGE_END = ('.png', '.jpg', '.jpeg')
PDF_END = ('.pdf')

class Document:
    def __init__(self) -> None:
        self.pages: List[Page] = []
        self.templates: List[Templayte] = []
        self.path: str


    def set_from_path(self, path_file):
        if path_file.lower().endswith(IMAGE_END):
            image = Image()
            image.set_img_from_path(path_file)
            page = Page(image=image)
            self.pages.append(page)
        elif path_file.lower().endswith(PDF_END):
            images = convert_from_path(path_file)
        
            for im in images:
                image = Image(img=np.array(im))
                page = Page(image=image)
                self.pages.append(page)