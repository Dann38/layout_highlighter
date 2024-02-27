from ..base_cluster_word_bold_extractor import BaseClusterWordBoldExtractor
from  img_doc.document.page import Word
from typing import List

import numpy as np

PERMISSIBLE_H_BBOX = 5  # that height bbox after which it makes no sense сrop bbox
PERMISSIBLE_W_BBOX = 3

class PsBoldExtractor(BaseClusterWordBoldExtractor):
    def __init__(self, boolean=True) -> None:
        super().__init__()
        self.boolean = boolean

    def extract(self, words: List[Word], gray_img: np.ndarray):
        for word in words:
            bold_val = self.evaluation_words(word.segment.get_segment_from_img(gray_img, delta=2))
            word.set_bold(bold_val)
        if self.boolean:
            x_vec = self.__get_prop_vectors(np.array([word.bold  for word in words]))
            bold_vals = self.clusterize(x_vec).tolist()
            for bold, word in zip(bold_vals, words):
                word.bold = int(bold)

    def __get_prop_vectors(self, x: np.ndarray) -> np.ndarray:
        nearby_x = x.copy()
        nearby_x[:-1] += x[1:] 
        nearby_x[1:] += x[:-1]
        nearby_x[0] += x[0] 
        nearby_x[-1] += x[-1] 
        nearby_x = nearby_x / 3.
        return np.stack((x, ), 1)
            
    def evaluation_words(self, image: np.ndarray) -> float:
        base_line_image = self._get_base_line_image(image)  # baseline - main font area
        base_line_image_without_sparces = self._get_rid_spaces(base_line_image)  # removing spaces from a string

        p_img = base_line_image[:, :-1] - base_line_image[:, 1:]
        p_img[abs(p_img) > 0] = 1.
        p_img[p_img < 0] = 0.
        p = p_img.mean() if p_img.shape[0] > 1 and p_img.shape[1] > 1  else 1
        
        word_mean = base_line_image_without_sparces.mean() if base_line_image_without_sparces.shape[0] > 1 and base_line_image_without_sparces.shape[1] > 1 else 0
        s = 1 - word_mean
        h = base_line_image.shape[0]
        if p==0 or h==0:
            evaluation = 1.
        else:
            evaluation = s/p/h 
        return evaluation
    
    def _get_rid_spaces(self, image: np.ndarray) -> np.ndarray:
        x = image.mean(0)
        not_space = x < 0.95
        if len(not_space) > PERMISSIBLE_W_BBOX:
            return image
        return image[:, not_space]

    def _get_base_line_image(self, image: np.ndarray) -> np.ndarray:
        h = image.shape[0]
        if h < PERMISSIBLE_H_BBOX:
            return image
        
        

        mean_ = image.mean(1)

        w = image.shape[1]
        if w < h*2:
            not_space = mean_ < 0.95
            return image[not_space, :]
        # delta_mean = abs(mean_[:-1] - mean_[1:])

        # max1 = 0
        # max2 = 0
        # argmax1 = 0
        # argmax2 = 0
        # for i, delta_mean_i in enumerate(delta_mean):
        #     if delta_mean_i <= max2:
        #         continue
        #     if delta_mean_i > max1:
        #         max2 = max1
        #         argmax2 = argmax1
        #         max1 = delta_mean_i
        #         argmax1 = i
        #     else:
        #         max2 = delta_mean_i
        #         argmax2 = i
        # h_min = min(argmax1, argmax2)
        # h_max = min(max(argmax1, argmax2) + 1, h)
                
        a1 = mean_.min()
        a2 = mean_.max()
        mean_len = len(mean_)
        c_min = mean_len
        h_min = 0
        h_max = len(mean_)-1
        for b1 in range(mean_len//2):
            for b2 in range(mean_len//2, mean_len):
                c1 = ((mean_[:b1] - a2)**2).sum()
                c2 = ((mean_[b1:b2] - a1)**2).sum()
                c3 = ((mean_[b2:] - a2)**2).sum()
                
                c = c1+c2+c3
                if c_min > c:
                    c_min = c
                    h_min = b1
                    h_max = b2
        if h_max-h_min < PERMISSIBLE_H_BBOX:
            return image
        return image[h_min:h_max, :]