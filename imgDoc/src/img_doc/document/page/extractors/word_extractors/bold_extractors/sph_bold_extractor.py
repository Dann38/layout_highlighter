import numpy as np
from img_doc.image import Image
MIN_H = 5

class SPHBoldExtractor:
    def __init__(self):
        pass
    
    def extract(self, page:"Page", conf):
        # page.resize(4)
        gray_img = page.image.get_binary_image()
        for word in page.words:
            
            img_word = Image(word.segment.get_segment_from_img(gray_img))
            # img_word.resize(8)
            word.set_bold(self.evaluation_word_img(img_word.img))

    def evaluation_word_img(self, img_word: np.ndarray) -> float:
        s = self._get_s_word_img(img_word)
        p = self._get_p_word_img(img_word)
        h = self._get_h_word_img(img_word)
        # return p

        if p==0 or s==0 or h==0:
            return 1.
        else:
            return s/p/h
    
    def _get_s_word_img(self, img_word: np.ndarray) -> float:
        img_word_inv = 1-img_word
        return img_word_inv.sum()
    
    def _get_p_word_img(self, img_word: np.ndarray) -> float:
        img1 = img_word + 1
        img_p = img1[:, 1:] -img_word[:, :-1]
        # img_p[img_p == 0] = 2
        img_p[img_p == 1] = 0
        img_p[img_p == 2] = 1
        return img_p.sum()

    def _get_h_word_img(self, img_word: np.ndarray) -> float:
        h, w = img_word.shape
        if h < MIN_H:
            return h
        
        mean_ = img_word.mean(1)
        if 2*w < h:
            not_space = mean_ < 0.95
            return len(not_space)

        a1 = mean_.min()
        a2 = mean_.max()
        mean_len = len(mean_)
        c_min = np.inf
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

        if h_max-h_min < MIN_H:
            return h

        return h_max-h_min

