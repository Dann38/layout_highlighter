import numpy as np
from img_doc.data_structures import Page, Image
from .. import BasePageExtractor

from img_doc.extractors.word_extractors import BaseWordExtractor
from img_doc.extractors.block_extractors.block_extractor_from_word import BaseBlockExtractorFromWord
from img_doc.extractors.block_extractors.block_label_extractor import BaseBlockLabelExtractor

from img_doc.extractors.word_extractors.word_extractor_from_img import TesseractWordExtractor 
from img_doc.extractors.block_extractors.block_extractor_from_word import KMeanBlockExtractor
from img_doc.extractors.block_extractors.block_label_extractor import MLPExtractor


class W2BExtractor(BasePageExtractor):
    def __init__(self, word_ext: BaseWordExtractor=TesseractWordExtractor(), 
                 block_ext: BaseBlockExtractorFromWord=KMeanBlockExtractor(),
                 block_label_ext: BaseBlockLabelExtractor=MLPExtractor("/build/models/mlp_len-micro_5.sav", {"len_vec": 5})) -> None:
        super().__init__()
        self.word_ext = word_ext
        self.block_ext = block_ext
        self.block_label_ext = block_label_ext
        
        self.save_no_join_blocks = False
        self.save_neighbors = False
        self.save_distans = False
        self.save_graph = False

        self.set_dist_row = None
        self.set_dist_word = None 

    def extract_from_image(self, image: Image) -> Page:
        words = self.word_ext.extract_from_img(image.img)
        history = self.get_history()
        blocks = self.block_ext.extract_from_word(words=words, history=history)
        self.block_label_ext.extract(blocks)
        page = Page(blocks=blocks, words=words, image=image, processing_info=history)
        return page


    def get_history(self):
        history = {        
            "join_blocks": [],
            "dist_word": "auto" if self.set_dist_word is None else self.set_dist_word ,
            "dist_row": "auto" if self.set_dist_row is None else self.set_dist_row,
        }

        if self.save_no_join_blocks:
            history["no_join_blocks"] = []
        if self.save_neighbors: 
            history["neighbors"] = []
        if self.save_distans:
            history["distans"] = []
        if self.save_graph:
            history["graph"] = None
        
        return history