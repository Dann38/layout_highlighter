from ..base_page_block_classificator import BasePageBlockClassificator
from img_doc.document.page.extractors.block_extractors.block_classificators.word_classificators import BaseWordBlockClassificator, BLOCK_LABEL
import numpy as np
import tensorflow as tf
from typing import List
from img_doc.image import SetImageSegment

class PageAndWordClassificator(BasePageBlockClassificator):
    def __init__(self, word_classificator: BaseWordBlockClassificator, conf) -> None:
        self.word_classificator = word_classificator 
        self.properties = conf["properties"]
        self.model = None
        if "path_model" in conf:
            self.model = tf.saved_model.load(conf["path_model"])

    def classification(self, page: "Page"):
        rez = self.page_classification(page)
        for block, rez_i in zip(page.blocks, rez):
            block.label = BLOCK_LABEL[np.argmax(rez_i)]

    def page_classification(self, page: "Page"):
        vecs = self.get_block_and_page_vecs(page)
        if self.model:
            return self.model(np.array(vecs))
        
    def get_block_and_page_vecs(self, page: "Page"):
        if "place_in_page" in self.properties:
            page.extract_place_in_page_for_block_segments()
        vecs = []
        vecs_blocks_on_page = self.get_blocks_vecs(page)
        for block, vec_block_on_page in zip(page.blocks, vecs_blocks_on_page):
            vec_block = self.word_classificator.get_block_vec(block)
            
            vecs.append(np.concatenate((vec_block, vec_block_on_page), axis=0)) 
        return vecs

    def get_blocks_vecs(self, page: "Page"):
        self.set_segments = SetImageSegment([block.segment for block in page.blocks])
        self.page = page
        len_vec = len(self.get_node_vec(0)) 
        count_vec = len(self.set_segments.segments)
        vecs = np.zeros((count_vec, len_vec))
        
        for i_node in range(len(self.set_segments.segments)):
            vecs[i_node, :] = self.get_node_vec(i_node) 
        
        return vecs
    

    def get_node_vec(self, i_node):
        properties_list = {
            "place_in_page": lambda: self.set_segments.get_info_segment(i_node, "place_in_page"),
            "count_word_in_page": lambda: [len(self.page.blocks[i_node].words)/len(self.page.words)],
        }
        rez = np.array([])
        for p in self.properties:
            vec_p = properties_list[p]()
            rez = np.concatenate((rez, vec_p), axis=0)
        return rez
    

    

    
    