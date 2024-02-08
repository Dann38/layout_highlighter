from typing import List
import numpy as np
from abc import abstractmethod

from img_doc.extractors.block_extractors.block_extractor_from_word import KMeanBlockExtractor
from ..base_block_label_extractor import BaseBlockLabelExtractor, Block, LABEL, Word
import pickle
import tensorflow as tf

class BaseVecExtractor(BaseBlockLabelExtractor):
    def __init__(self, param):
        self.kmean_ext = KMeanBlockExtractor()
        if "path_model" in param: 
            self.load_model = tf.saved_model.load(param["path_model"])
        self.param = param

    def extract(self, blocks: List[Block]) -> None:
        for block in blocks:
            words = block.words
            vec = self.get_vec_from_words(words)
            rez = self.load_model(np.array([vec], dtype="float32"))[0]
            class_model = [LABEL["text"], LABEL["header"], LABEL["list"], LABEL["table"], LABEL["no_struct"]]
            block.label = class_model[rez]
    
    @abstractmethod
    def get_vec_from_words(self, words: List[Word]) -> np.ndarray:
        pass
        
