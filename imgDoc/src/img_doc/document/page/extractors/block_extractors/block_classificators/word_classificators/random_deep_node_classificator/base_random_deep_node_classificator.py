from typing import List
from ..base_word_classificators import BaseWordBlockClassificator
from img_doc.image import SetImageSegment
import numpy as np
"""
По словам формируется граф и из него выбираются случайные узлы.
Из каждого узла извлекаются свойства и из его соседей заданного уровнея.
В результате формируется вектор.
Длина вектора есть (4^D-1)/3 * N *M, 
N - число узлов, M - вектор характеризующий узел, D - глубина 
"""


class BaseRandomDeepNodeClassificator(BaseWordBlockClassificator):
    def __init__(self, conf) -> None:
        super().__init__(conf)
        self.properties = conf["properties"]
        self.count_node = conf["count_node"]
        self.deep = conf["deep"]

    def get_words_vec(self, words):
        self.set_segments = SetImageSegment([word.segment for word in words])
        self.set_segments.extract_neighbors()
        rnd_nodes = self.set_segments.get_list_random_node(self.count_node)
        
        len_node_vec = len(self.get_deep_node_vec(0, self.deep)) 
        len_vec = self.count_node*len_node_vec
        vec = np.zeros(len_vec)

        
        for i, i_node in enumerate(rnd_nodes):
            vec[len_node_vec*i:len_node_vec*(i+1)] = self.get_deep_node_vec(i_node, self.deep) 
        
        for i in range(len_node_vec):
            max_ = np.max(np.abs(vec[i::len_node_vec]))
            vec[i::len_node_vec] = vec[i::len_node_vec]/max_ if max_ != 0 else vec[i::len_node_vec]
        # vec[vec == np.inf] = 1.0
        # vec[vec == -np.inf] = -1.0
        return vec
    

    def get_deep_node_vec(self, i_node, max_level):
        rez = self.get_next_deep_node_vec(i_node, max_level)
        return rez

    def get_next_deep_node_vec(self, i_node, level):
        rez = self.get_node_vec(i_node)
        if level!=0:
            for j_node in self.set_segments.neighbors[i_node]:
                rez_j = self.get_next_deep_node_vec(j_node, level-1)
                rez = np.concatenate((rez, rez_j), axis=0)
        return rez

    def get_node_vec(self, i_node):
        properties_list = {
            "many_dist": lambda: self.set_segments.get_many_dist(i_node),
            "many_angle": lambda: self.set_segments.get_many_angle(i_node),
            "place_in_block": lambda: self.set_segments.get_info_segment(i_node, "place_in_block"),
            "bold": lambda: self.set_segments.get_info_segment(i_node, "bold"),
            "height": lambda: self.set_segments.get_height(i_node),
        }
        
        rez = np.array([])
        for p in self.properties:
            vec_p = properties_list[p]()
            rez = np.concatenate((rez, vec_p), axis=0)
        return rez
    

    

    
    