from ..base_bold_extractor import BaseWordExtractor, Word, ImageSegment
from typing import List
from .base_clasterizer import BoldAgglomerativeClusterizer
import cv2
import numpy as np

PERMISSIBLE_H_BBOX = 5  # that height bbox after which it makes no sense сrop bbox
PERMISSIBLE_W_BBOX = 3

class ISPBoldExtractor(BaseWordExtractor):
    def __init__(self):
        self.permissible_h_bbox = 5
        self.clusterizer = BoldAgglomerativeClusterizer()

    def extract(self, words: List[Word], image: np.ndarray) :
        if len(words) == 0:
            return 

        if len(words) == 1:
            return words[0].set_bold(0.0)

        bboxes_evaluation = self.__get_bboxes_evaluation(image, words)
        bold_probabilities = self.__clusterize(bboxes_evaluation)
        for i, word in enumerate(words):
            word.set_bold(bold_probabilities[i])
           
            


    def __get_bboxes_evaluation(self, image: np.ndarray, words: List[Word]):
        bboxes_evaluation = [self.__evaluation_one_bbox_image(word.segment.get_segment_from_img(image)) for word in words]
        return bboxes_evaluation

    def __evaluation_one_bbox_image(self, image: np.ndarray) -> float:
        base_line_image = self.__get_base_line_image(image)
        base_line_image_without_spaces = self.__get_rid_spaces(base_line_image)

        p_img = base_line_image[:, :-1] - base_line_image[:, 1:]
        p_img[abs(p_img) > 0] = 1.
        p_img[p_img < 0] = 0.
        p = p_img.mean()

        s = 1 - base_line_image_without_spaces.mean()

        if p > s or s == 0:
            evaluation = 1.
        else:
            evaluation = p / s
        return evaluation
        # base_line_image = self.__get_base_line_image(image)  # baseline - main font area
        # h = max(100, base_line_image.shape[0])
        # image = cv2.resize(base_line_image, dsize=(h, round(h*base_line_image.shape[1]/base_line_image.shape[0])), interpolation=cv2.INTER_LINEAR)
        # base_line_image = image
        # p_img = base_line_image[:, :-1] - base_line_image[:, 1:]
        # p_img[abs(p_img) > 0] = 1.
        # p_img[p_img < 0] = 0.
        # p = p_img.sum() if p_img.shape[0] > 1 and p_img.shape[1] > 1  else p_img.shape[0]*p_img.shape[1]
        
        # s_img = 1 - self.__get_rid_spaces(base_line_image)  # removing spaces from a string
        # s = s_img.sum() if s_img.shape[0] > 1 and s_img.shape[1] > 1 else 0
        
        # # h = base_line_image.shape[0] if base_line_image.shape[0]>0 else 1
        # if p*h == 0:
        #     return 1
        # evaluation = s/(p*h)
        # # evaluation = s/p 
        # return evaluation

    def __clusterize(self, bboxes_evaluation: List[float]) -> List[float]:
        vector_bbox_evaluation = np.array(bboxes_evaluation)
        vector_bbox_indicators = self.clusterizer.clusterize(vector_bbox_evaluation)
        bboxes_indicators = vector_bbox_indicators.tolist()
        return bboxes_indicators

    def __get_rid_spaces(self, image: np.ndarray) -> np.ndarray:
        x = image.mean(0)
        not_space = x < 0.95
        if len(not_space) > 3:
            return image
        return image[:, not_space]

    def __get_base_line_image(self, image: np.ndarray) -> np.ndarray:
        h = image.shape[0]
        if h < self.permissible_h_bbox:
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
        if h_max - h_min < self.permissible_h_bbox:
            return image
        return image[h_min:h_max, :]
