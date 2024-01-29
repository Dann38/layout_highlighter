from ..base_bold_extractor import BaseWordExtractor, Word, ImageSegment
from typing import List
import cv2 
import numpy as np

PERMISSIBLE_H_BBOX = 5  # that height bbox after which it makes no sense сrop bbox
PERMISSIBLE_W_BBOX = 3

class WidthBoldExtractor(BaseWordExtractor):
    def extract(self, words: List[Word], gray_img: np.ndarray) -> List[Word]:
        for word in words:
            bold_val = self.evaluation_words(word.segment.get_segment_from_img(gray_img))
            bold = 0 if bold_val < 1 else 1
            word.set_bold(bold)

            
    def evaluation_words(self, image: np.ndarray) -> float:
        
        base_line_image = self._get_base_line_image(image)  # baseline - main font area
        # h = 30
        # image = cv2.resize(base_line_image, dsize=(h, round(h*base_line_image.shape[1]/base_line_image.shape[0])), interpolation=cv2.INTER_LINEAR)
        # base_line_image = image
        p_img_x = base_line_image[:, :-1] - base_line_image[:, 1:]
        p_img_y = base_line_image[:-1, :] - base_line_image[:1, :]
        p_img_x[abs(p_img_x) > 0] = 1.
        p_img_x[p_img_x < 0] = 0.
        p_img_y[abs(p_img_y) > 0] = 1.
        p_img_y[p_img_y < 0] = 0.
        p = p_img_x.sum()+p_img_y.sum() if p_img_x.shape[0] > 1 and p_img_x.shape[1] > 1  else p_img.shape[0]*p_img.shape[1]
        
        s_img = 1 - self._get_rid_spaces(base_line_image)  # removing spaces from a string
        s = s_img.sum() if s_img.shape[0] > 1 and s_img.shape[1] > 1 else 0
        
        # h = base_line_image.shape[0] if base_line_image.shape[0]>0 else 1
        if p == 0:
            return 1
        evaluation = 2*s/p
        # evaluation = s/p 
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
        delta_mean = abs(mean_[:-1] - mean_[1:])

        max1 = 0
        max2 = 0
        argmax1 = 0
        argmax2 = 0
        for i, delta_mean_i in enumerate(delta_mean):
            if delta_mean_i <= max2:
                continue
            if delta_mean_i > max1:
                max2 = max1
                argmax2 = argmax1
                max1 = delta_mean_i
                argmax1 = i
            else:
                max2 = delta_mean_i
                argmax2 = i
        h_min = min(argmax1, argmax2)
        h_max = min(max(argmax1, argmax2) + 1, h)
        if h_max-h_min < PERMISSIBLE_H_BBOX:
            return image
        return image[h_min:h_max, :]