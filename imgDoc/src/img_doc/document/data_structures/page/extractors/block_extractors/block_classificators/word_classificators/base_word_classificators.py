from img_doc.document.data_structures.page.data_structures import Block, Word, BLOCK_LABEL
from ..base_block_classificator import BaseBlockClassificator
from typing import List
import numpy as np
from abc import abstractmethod

"""
Гипотеза в том, что для определения вида блока достаточно информацию 
"""
class BaseWordBlockClassificator(BaseBlockClassificator):
    def classification(self, block: Block):
        rez = self.words_classification(block.words)
        block.label = BLOCK_LABEL[np.argmax(rez)]

    @abstractmethod
    def words_classification(self, words: List[Word]) -> List[float]:
        pass