from typing import List, Dict, Any
from . import Block, Word
from ..image import Image


class Page:
    def __init__(self, image:Image = None, blocks:List[Block] = None, words: List[Word] = None,
                 processing_info: Dict[str, Any] = None ) -> None:
        self.blocks = blocks
        self.image = image
        self.words = words
        self.processing_info = processing_info

    def to_dict(self):
        page_dict = self.processing_info
        page_dict["words"] = [word.to_dict() for word in self.words]
        page_dict["join_blocks"] = [block.to_dict() for block in self.blocks]
        if "no_join_blocks" in page_dict.keys():
            page_dict["no_join_blocks"] = [block.to_dict() for block in page_dict["no_join_blocks"]]
        return page_dict