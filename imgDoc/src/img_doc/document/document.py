from pdf2image import convert_from_path, convert_from_bytes
from .page import Page
from .templayte import Templayte
from typing import List
import numpy as np

IMAGE_END = ('.png', '.jpg', '.jpeg')
PDF_END = ('.pdf')

class Document:
    def __init__(self) -> None:
        self.pages: List[Page] = []
        self.templates: List[Templayte] = []
        self.path: str
        self.metadata: dict


    def set_from_path(self, path_file):
        self.path = path_file
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

    def update_image_from_path(self, path_file): # need for dataset extractors
        self.path = path_file
        if path_file.lower().endswith(IMAGE_END):
            self.pages[0].set_from_path(path_file)
        elif path_file.lower().endswith(PDF_END):
            images = convert_from_path(path_file)
            for i, im in enumerate(images):
                self.pages[i].set_from_np(np.array(im))