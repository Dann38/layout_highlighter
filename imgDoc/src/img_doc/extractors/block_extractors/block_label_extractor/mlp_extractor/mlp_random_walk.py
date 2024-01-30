from typing import List
import numpy as np

from img_doc.extractors.block_extractors.block_extractor_from_word import KMeanBlockExtractor
from ..base_block_label_extractor import BaseBlockLabelExtractor, Block, LABEL
import pickle

class MLPRandomWalkExtractor(BaseBlockLabelExtractor):
    def __init__(self, filename, param):
        self.kmean_ext = KMeanBlockExtractor()
        self.load_model = pickle.load(open(filename, 'rb')) 
        self.param = param

    def extract(self, blocks: List[Block]) -> None:
        for block in blocks:
            words = block.words
            vec = self.get_vec_from_words(words, len_vec=self.param["len_vec"])
            rez = self.load_model.predict(np.array([vec]))[0]
            class_model = [LABEL["text"], LABEL["header"], LABEL["list"], LABEL["table"], LABEL["no_struct"]]
            
            block.label = class_model[np.argmax(rez)]
    

    def get_vec_from_words(self, words, len_vec=5):
        rng = np.random.default_rng()
        if len(words) == 0:
            return np.zeros(len_vec)
        neighbors = self.kmean_ext.get_index_neighbors_word(words)
        distans = self.kmean_ext.get_distans(neighbors, words)
        old_node = 0
        vec = np.zeros(len_vec)
        for i in range(len_vec):
            r = rng.integers(4)
            new_node = neighbors[old_node][r]
            vec[i] = distans[old_node][r]
            
            old_node = new_node
        
        return vec if vec.sum()==0 else vec/vec.sum()
