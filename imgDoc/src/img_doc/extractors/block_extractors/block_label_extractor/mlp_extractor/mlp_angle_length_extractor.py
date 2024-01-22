from typing import List
import numpy as np
from img_doc.extractors.block_extractors.block_extractor_from_word import KMeanBlockExtractor
from ..base_block_label_extractor import BaseBlockLabelExtractor, Block, LABEL
import pickle

class MLPAngLenExtractor(BaseBlockLabelExtractor):
    def __init__(self, filename, param):
        self.kmean_ext = KMeanBlockExtractor()
        self.load_model = pickle.load(open(filename, 'rb')) 
        self.param = param

    def extract(self, blocks: List[Block]) -> None:
        for block in blocks:
            words = block.words
            vec = self.get_vec_from_words(words, len_vec=self.param["len_vec"])
            rez = self.load_model.predict(np.array([vec]))[0]
            class_model = [LABEL["text"], LABEL["header"], LABEL["list"]]
            
            block.label = class_model[np.argmax(rez)]
    

    def get_vec_from_words(self, words, len_vec=5):
        if len(words) == 0:
            return np.zeros(2*len_vec)
        neighbors = self.kmean_ext.get_index_neighbors_word(words)
        distans = self.kmean_ext.get_distans(neighbors, words)
        vec = np.ravel(np.array(distans))
        max_vec = vec.max()
        vec = vec/max_vec if max_vec != 0 else vec
        vec, _ = np.histogram(vec, np.linspace(0, 1, len_vec+1))
        normal = np.linalg.norm(vec)
        vec_length = vec/normal if normal > 0 else vec
        vec_ang = []
        for i, neighbor in enumerate(neighbors):
            for neig in neighbor:
                x1, y1 = words[i].segment.get_center() 
                x2, y2 = words[neig].segment.get_center() 
                den = ((y1-y2)**2 + (x1-x2)**2)**0.5
                num = abs(x1-x2)
                if den != 0:
                    vec_ang.append(num/den)
        vec, _ = np.histogram(vec_ang, np.linspace(0, 1, len_vec+1))
        normal = np.linalg.norm(vec)
        vec_ang = vec/normal if normal > 0 else vec    
        return np.concatenate((vec_length, vec_ang), axis = None)
