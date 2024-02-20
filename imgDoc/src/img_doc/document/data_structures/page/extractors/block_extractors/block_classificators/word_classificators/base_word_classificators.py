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
        rez = self.block_classification(block)
        block.label = BLOCK_LABEL[np.argmax(rez)]

    def block_classification(self, block: Block)-> List[float]:
        vec = self.get_block_vec(block)
        rez = None
        if self.model:
            rez = self.model(np.array[vec])
        return rez 
        
    
    def get_block_vec(self, block: Block):
        block.extract_place_in_block_word_segments()
        return self.get_words_vec(block.words)

    @abstractmethod
    def get_words_vec(self, words):
        pass

