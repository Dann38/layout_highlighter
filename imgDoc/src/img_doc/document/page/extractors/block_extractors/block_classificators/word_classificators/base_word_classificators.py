from ..base_block_classificator import BaseBlockClassificator, BLOCK_LABEL
from typing import List
import numpy as np
from abc import abstractmethod

"""
Гипотеза в том, что для определения вида блока достаточно информацию 
"""
class BaseWordBlockClassificator(BaseBlockClassificator):
    def classification(self, block: "Block"):
        rez = self.block_classification(block)
        block.label = BLOCK_LABEL[np.argmax(rez)]

    def block_classification(self, block: "Block")-> List[float]:
        vec = self.get_block_vec(block)
        rez = None
        if self.model:
            rez = self.model(np.array([vec]))
        return rez[0] 
        
    
    def get_block_vec(self, block: "Block"):
        block.extract_place_in_block_for_word_segments()
        block.extract_bold_for_word_segments() # перенос свойства bold из слова в информацию о сегменте.

        return self.get_words_vec(block.words)

    @abstractmethod
    def get_words_vec(self, words):
        pass

