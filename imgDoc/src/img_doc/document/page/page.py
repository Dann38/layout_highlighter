from typing import List
from img_doc.image import Image, ImageSegment
from .word import Word
from .block import Block
from .extractors import Words2Paragraph, TesseractWordExtractor, SPHBoldExtractor
from .extractors.block_extractors import BaseRandomWalkClassificator, BaseRandomDeepNodeClassificator, PageAndWordClassificator

PARAGRAPH_EXTRACTORS = {
    "words2paragraph": Words2Paragraph()
}

WORD_EXTRACTORS = {
    "tesseract": TesseractWordExtractor()
}

BOLD_EXTRACTORS = {
    "sph": SPHBoldExtractor()
}

BLOCK_CLASSIFICATOR = {
    "page_and_deep": BaseRandomDeepNodeClassificator,
    "page_and_walk": BaseRandomWalkClassificator
}

class Page:
    def __init__(self) -> None:
        self.image: Image
        self.blocks: List[Block] = []
        self.words: List[Word] = []
        # self.processing_info = processing_info
    
    def to_dict(self):
        dict_page = dict()
        dict_page["words"] = [word.to_dict() for word in self.words]
        dict_page["blocks"] = [block.to_dict() for block in self.blocks]
        return dict_page



    def set_from_path(self, path):
        self.image = Image()
        self.image.set_img_from_path(path)

    def set_from_np(self, np_array):
        self.image = Image(img=np_array)

    def extract_paragraphs(self, method:str = "words2paragraph", conf={}):
        PARAGRAPH_EXTRACTORS[method].extract(self, conf)

    def extract_word(self, method:str = "tesseract", conf={}):
        WORD_EXTRACTORS[method].extract(self, conf)

    def extract_word_bold(self, method:str = "sph", conf={}):
        BOLD_EXTRACTORS[method].extract(self, conf)

    def set_words_from_dict(self, list_words: List[dict]):
        self.words = []
        for dict_word in list_words:
            word = Word(dict_word)
            self.words.append(word)

    def extract_place_in_page_for_block_segments(self):
        page_h = self.image.segment.get_height()
        page_w = self.image.segment.get_width()
        page_dict = self.image.segment.get_segment_2p()
        x0, y0 = page_dict["x_top_left"],page_dict["y_top_left"] 
        for block in self.blocks:
            block_dict = block.segment.get_segment_2p()
            x1, y1 = block_dict["x_top_left"], block_dict["y_top_left"]
            block.segment.add_info("place_in_page",((x1-x0)/page_w, (y1-y0)/page_h))

    def set_blocks_from_dict(self, list_blocks: List[dict]):
        self.blocks = []
        for dict_block in list_blocks:
            block = Block(dict_block)
            self.blocks.append(block)

    def get_block_from_segment(self, segment: ImageSegment, conf) -> Block:
        block = Block(segment.get_segment_2p())
        self.extract_word(conf["extractor_word"]["method"],conf["extractor_word"]["conf"])
        for word in self.words:
            if block.segment.is_intersection(word.segment):
                block.words.append(word)
        if "page_classification" in conf:
            self.extract_word_bold()
            self.blocks = [block] #TODO Придумать как сделать без затирания блоков
            self.classification_block(conf["page_classification"])
            return self.blocks[0]
        else:
            block.classification(conf["classification"])
            return block
    
    def classification_block(self, conf):
        rnd_classifier = BLOCK_CLASSIFICATOR[conf["type"]](conf["rnd_conf"])
        classifier = PageAndWordClassificator(rnd_classifier, conf["conf"])
        classifier.classification(self)

    def resize(self, k):
        self.image.resize(k)
        for block in self.blocks:
            block.segment.resize(k, resize_word=False)
        for word in self.words:
            word.segment.resize(k)