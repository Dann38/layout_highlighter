from typing import List
from . import Block
from ..image import Image

class Page:
    def __init__(self, image:Image = None, blocks:List[Block] = None) -> None:
        self.blocks = blocks
        self.image = image
