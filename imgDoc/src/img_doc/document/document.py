from pdf2image import convert_from_path, convert_from_bytes
from .data_structures import Page, Templayte
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
            page = Page()
            page.set_from_path(path_file)
            self.pages.append(page)
        elif path_file.lower().endswith(PDF_END):
            images = convert_from_path(path_file)
            for im in images:
                page = Page()
                page.set_from_np(np.array(im))
                self.pages.append(page)