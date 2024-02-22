from typing import List
from ..base_word_classificators import BaseWordBlockClassificator
from img_doc.image import SetImageSegment
import numpy as np
import tensorflow as tf
"""
По словам формируется граф и по нему осуществляются случайные блуждания.
Из каждого узла извлекаются свойства из которых формируется вектор.
Длина вектора есть N*M, N - число шагов, M - вектор характеризующий узел.
"""


class BaseRandomWalkClassificator(BaseWordBlockClassificator):
    def __init__(self, conf) -> None:
        self.properties = conf["properties"]
        self.count_step = conf["count_step"]
        self.model = None
        if "path_model" in conf:
            self.model = tf.saved_model.load(conf["path_model"])
    
    def get_words_vec(self, words):
        self.set_segments = SetImageSegment([word.segment for word in words])
        self.set_segments.extract_neighbors()

        rnd_walk = self.set_segments.get_rnd_walk(self.count_step+1)
        len_node_vec = len(self.get_node_vec(0, 0)) 
        len_vec = self.count_step*len_node_vec
        vec = np.zeros(len_vec)

        
        for i, i_node in enumerate(rnd_walk[:-1]):
            j_node = rnd_walk[i+1]
            vec[len_node_vec*i:len_node_vec*(i+1)] = self.get_node_vec(i_node, j_node) 
        
        for i in range(len_node_vec):
            max_ = np.max(np.abs(vec[i::len_node_vec]))
            vec[i::len_node_vec] = vec[i::len_node_vec]/max_ if max_ != 0 else vec[i::len_node_vec]
        # vec[vec == np.inf] = 1.0
        # vec[vec == -np.inf] = -1.0
        return vec
    

    def get_node_vec(self, i_node, j_node):
        properties_list = {
            "dist": lambda: self.set_segments.get_many_dist(i_node, j_node),
            "many_dist": lambda: self.set_segments.get_many_dist(i_node),
            "many_angle": lambda: self.set_segments.get_many_angle(i_node),
            "place_in_block": lambda: self.set_segments.get_place_in_block(i_node),
        }
        rez = np.array([])
        for p in self.properties:
            vec_p = properties_list[p]()
            rez = np.concatenate((rez, vec_p), axis=0)
        return rez
    

    

    
    