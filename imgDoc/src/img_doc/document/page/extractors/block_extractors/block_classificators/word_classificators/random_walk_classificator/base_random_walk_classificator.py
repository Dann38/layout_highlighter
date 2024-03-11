from typing import List
from ..base_word_classificators import BaseWordBlockClassificator
from img_doc.image import SetImageSegment
import numpy as np
"""
По словам формируется граф и по нему осуществляются случайные блуждания.
Из каждого узла извлекаются свойства из которых формируется вектор.
Длина вектора есть N*M, N - число шагов, M - вектор характеризующий узел.
"""


class BaseRandomWalkClassificator(BaseWordBlockClassificator):
    def __init__(self, conf) -> None:
        super().__init__(conf)
        self.count_step = conf["count_step"]
        
    def get_vec_each_segment(self, set_segments):
        self.set_segments = set_segments

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
            "place_in_block": lambda: self.set_segments.get_info_segment(i_node, "place_in_block"),
            "bold": lambda: self.set_segments.get_info_segment(i_node, "bold"),
            "height": lambda: self.set_segments.get_height(i_node),
        }
        rez = np.array([])
        for p in self.properties:
            if p in properties_list:
                vec_p = properties_list[p]()
                rez = np.concatenate((rez, vec_p), axis=0)
        return rez
    

    

    
    