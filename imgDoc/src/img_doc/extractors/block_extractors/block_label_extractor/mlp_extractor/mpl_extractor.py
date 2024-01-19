from typing import List
import numpy as np
from img_doc.extractors.block_extractors.block_extractor_from_word import KMeanBlockExtractor
from ..base_block_label_extractor import BaseBlockLabelExtractor, Block, LABEL
import pickle

class MLPExtractor(BaseBlockLabelExtractor):
    def __init__(self, filename):
        self.kmean_ext = KMeanBlockExtractor()
        self.load_model = pickle.load(open(filename, 'rb')) 


    def extract(self, blocks: List[Block]) -> None:
        for block in blocks:
            words = block.words
            vec = self.get_vec_from_words(words)
            rez = self.load_model.predict(np.array([vec]))[0]
            class_model = [2, 3, 4]
            
            block.label = class_model[np.argmax(rez)]
    # LABEL = {
    #     "no_struct": 0,
    #     "multiple_blocks": 1,
    #     "text": 2,
    #     "header": 3,
    #     "list": 4,
    #     "table": 5,
    # }

    def get_vec_from_words(self, words, len_vec=5):
        if len(words) == 0:
            return np.zeros(len_vec)
        neighbors = self.kmean_ext.get_index_neighbors_word(words)
        distans = self.kmean_ext.get_distans(neighbors, words)
        vec = np.ravel(np.array(distans))
        vec = vec/vec.max()
        vec, _ = np.histogram(vec, np.linspace(0, 1, len_vec+1))
        normal = np.linalg.norm(vec)
        vec = vec/normal if normal > 0 else vec
        return vec
