from abc import ABC, abstractmethod
from img_doc.data_structures import Word, Block, LABEL
from typing import List, Dict

class BaseBlockLabelExtractor:
    @abstractmethod
    def extract(self, blocks: List[Block]) -> None:
        pass

