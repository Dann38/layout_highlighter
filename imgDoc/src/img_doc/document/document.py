from pdf2image import convert_from_path, convert_from_bytes
from .page import Page, Block
from .templayte import Templayte
from typing import List
import numpy as np
from img_doc.image import ImageSegment 

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

    def update_image_from_path(self, path_file): # need for dataset extractors #TODO Проверить до сих пор нужен
        self.path = path_file
        if path_file.lower().endswith(IMAGE_END):
            self.pages[0].set_from_path(path_file)
        elif path_file.lower().endswith(PDF_END):
            images = convert_from_path(path_file)
            for i, im in enumerate(images):
                self.pages[i].set_from_np(np.array(im))

    def get_info_from_segment(self, num_page:int, x_top_left:int, y_top_left:int, x_bottom_right:int, y_bottom_right:int, conf:dict) -> Block:
        segment = ImageSegment(x_top_left, y_top_left, x_bottom_right, y_bottom_right)
        block = self.pages[num_page].get_block_from_segment(segment, conf)
        return block

