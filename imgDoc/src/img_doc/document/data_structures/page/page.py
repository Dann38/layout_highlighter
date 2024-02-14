from typing import List, Dict, Any
# from .data_structures.document import Block, Word
from .data_structures.image import Image
from .extractors import Words2Paragraph

class Page:
    def __init__(self) -> None:
        self.image: Image
        # self.blocks = blocks
        # self.words = words
        # self.processing_info = processing_info

    def to_dict(self):
        # page_dict = self.processing_info
        # page_dict["words"] = [word.to_dict() for word in self.words]
        # page_dict["join_blocks"] = [block.to_dict() for block in self.blocks]
        # if "no_join_blocks" in page_dict.keys():
        #     page_dict["no_join_blocks"] = [block.to_dict() for block in page_dict["no_join_blocks"]]
        return page_dict
    
    def set_from_path(self, path):
        self.image = Image()
        self.image.set_img_from_path(path)

    def set_from_np(self, np_array):
        self.image = Image(img=np_array)

    # def 

    # def extract_paragraphs(self, paragraph_ext = Words2Paragraph()):
    #     self.extract_words()
    #     paragraph_ext(self.image)