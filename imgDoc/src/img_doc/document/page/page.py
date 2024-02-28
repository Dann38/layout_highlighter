from typing import List
from img_doc.image import Image
from .word import Word
from .block import Block
from .extractors import Words2Paragraph, TesseractWordExtractor


PARAGRAPH_EXTRACTORS = {
    "words2paragraph": Words2Paragraph()
}

WORD_EXTRACTORS = {
    "tesseract": TesseractWordExtractor()
}

class Page:
    def __init__(self) -> None:
        self.image: Image
        self.blocks: List[Block] = []
        self.words: List[Word] = []
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

    def extract_paragraphs(self, method:str = "words2paragraph", conf={}):
        PARAGRAPH_EXTRACTORS[method].extract(self, conf)

    def extract_word(self, method:str = "tesseract", conf={}):
        WORD_EXTRACTORS[method].extract(self, conf)

    def set_words_from_dict(self, list_words: List[dict]):
        self.words = []
        for dict_word in list_words:
            word = Word(dict_word)
            self.words.append(word)

    def set_blocks_from_dict(self, list_blocks: List[dict]):
        self.blocks = []
        for dict_block in list_blocks:
            block = Block(dict_block)
            self.blocks.append(block)

    def get_block_from_segment(self, segment, conf) -> Block:
        block = Block()
        block.segment = segment
        img = block.segment.get_segment_from_img(self.image.img)
        list_words = WORD_EXTRACTORS[conf["extractor_word"]["method"]].extract_from_img(img, conf["extractor_word"]["conf"])
        block.set_words_from_dict(list_words)
        block.classification(conf["classification"])
        return block
    
    def resize(self, k):
        self.image.resize(k)
        for block in self.blocks:
            block.segment.resize(k, resize_word=False)
        for word in self.words:
            word.segment.resize(k)