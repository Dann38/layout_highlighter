from ..base_vec_extractor import BaseVecExtractor
import numpy as np

class MDistMAng(BaseVecExtractor):
    def get_vec_from_words(self, words):
        rng = np.random.default_rng()
        count_node = self.param["count_node"]
        vec = np.zeros(count_node*8)
        if len(words) == 0:
            return vec

        neighbors = self.kmean_ext.get_index_neighbors_word(words)
        distans = self.kmean_ext.get_distans(neighbors, words)
        old_node = rng.integers(len(words))
        
        for i in range(count_node):
            r = rng.integers(4)
            new_node = neighbors[old_node][r]
            for k in range(4):
                vec[i*8+k] = distans[old_node][k]
            for k in range(4):
                word1 = words[old_node]
                word2 = words[neighbors[old_node][k]]
                vec[i*8+4+k] = self.get_ang(word1, word2)
            old_node = new_node
        
        return vec if vec.sum()==0 else vec/vec.sum()

    def get_ang(self, word1, word2):
        x1, y1 = word1.segment.get_center() 
        x2, y2 = word2.segment.get_center() 
        den = ((y1-y2)**2 + (x1-x2)**2)**0.5
        num = abs(x1-x2)
        
        return num/den if den != 0 else 0.0