from typing import List
from img_doc.document.data_structures.page.data_structures import Word
from ..base_word_classificators import BaseWordBlockClassificator
from img_doc.document.data_structures.page.data_structures import SetImageSegment
import numpy as np
"""
По словам формируется граф и по нему осуществляются случайные блуждания.
Из каждого узла извлекаются свойства из которых формируется вектор.
Длина вектора есть N*M, N - число шагов, M - вектор характеризующий узел.
"""


class BaseRandomWalkClassificator(BaseWordBlockClassificator):
    def __init__(self, properties, count_step) -> None:
        self.properties = properties
        self.count_step = count_step


    def words_classification(self, words: List[Word]) -> List[float]:
        vec = self.get_words_vec(words)

        return [float]
    
    def get_words_vec(self, words):
        

        set_segments = SetImageSegment([word.segment for word in words])
        set_segments.extract_neighbors()

        rnd_walk = set_segments.get_rnd_walk(c)
        len_node_vec = len(self.get_node_vec(self.neighbors, 0, 0)) 
        len_vec = self.count_step*len_node_vec
        vec = np.zeros(len_vec)
        
        self.words = words

        return vec
    

    def get_node_vec(self, i_node):
        properties_list = {
            "dist": self.get_dist,
            "many_dist": self.get_many_dist,
            "many_angle": self.get_many_angle,

        }
        rez = np.array([])
        for p in self.properties:
            vec_p = properties_list[p]()
            rez = np.concatenate((rez, vec_p), axis=0)
        return rez
    

    

    
    