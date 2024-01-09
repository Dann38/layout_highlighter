from abc import ABC, abstractmethod
from img_doc.data_structures import Word, Block
from typing import List, Dict


class BaseBlockExtractorFromWord(ABC):
    @abstractmethod
    def extract_from_word(self, words: List[Word], history: Dict) -> List[Block]:
        pass

    def join_intersect_blocks(self, blocks: List[Block]) -> List[Block]:
        new_blocks = blocks
        run = True
        while run:
            old_blocks = new_blocks
            new_blocks = []
            for block in old_blocks:
                self.__add_block_in_new_list(new_blocks, block)
            if len(new_blocks) == len(old_blocks):
                run = False
        return new_blocks


    def __add_block_in_new_list(self, new_blocks, block):
        for new_block in new_blocks:
            if new_block.intersection(block):
                new_block.add_block_in_block(block)
                return
        new_blocks.append(block)
