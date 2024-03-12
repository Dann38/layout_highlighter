from ..base_block_classificator import BaseBlockClassificator, BLOCK_LABEL
from typing import List
import numpy as np
import tensorflow as tf
from img_doc.image import SetImageSegment

from abc import abstractmethod

"""
Гипотеза в том, что для определения вида блока достаточно информацию 
"""
class BaseWordBlockClassificator(BaseBlockClassificator):
    def __init__(self, conf) -> None:
        self.properties = conf["properties"]
        self.model = None
        if "path_model" in conf:
            self.model = tf.saved_model.load(conf["path_model"])

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
        if len(block.words) == 0:
            raise ValueError()
        if "place_in_block" in self.properties:
            block.extract_place_in_block_for_word_segments()
        if "bold" in self.properties or "hist_bold" in self.properties:
            block.extract_bold_for_word_segments() # перенос свойства bold из слова в информацию о сегменте.
        
        set_segments = SetImageSegment([word.segment for word in block.words])
        set_segments.extract_neighbors()

        word_vec = self.get_vec_each_segment(set_segments)
        block_vec = self.get_vec_set_segment(set_segments)

        return np.concatenate((word_vec, block_vec), axis=0)


    def get_vec_set_segment(self, set_segments: SetImageSegment):
        properties_list = {
            "hist_dist": lambda: set_segments.get_dist_hist(),
            "hist_ang": lambda: set_segments.get_ang_hist(),
            "hist_bold": lambda: set_segments.get_bold_hist(),
            "hist_height": lambda: set_segments.get_height_hist(),
        }
        rez = np.array([])
        for p in self.properties:
            if p in properties_list:
                vec_p = properties_list[p]()
                rez = np.concatenate((rez, vec_p), axis=0)
        return rez

    @abstractmethod
    def get_vec_each_segment(self, words):
        pass
