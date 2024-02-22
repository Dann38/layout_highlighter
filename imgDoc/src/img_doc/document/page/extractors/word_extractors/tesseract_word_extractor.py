import pytesseract
import numpy as np
from typing import List
import cv2
from .base_word_extractor import BaseWordExtractor

class TesseractWordExtractor(BaseWordExtractor):
    def extract(self, page: "Page", conf):        
        if not conf:
            word_list = self.extract_from_img(page.image.img)
        else:
            word_list = self.extract_from_img(page.image.img, conf)
        
        page.set_words_from_dict(word_list)
        
    def extract_from_img(self, img, conf={"lang": "eng+rus", "psm": 4, "oem": 3, "k": 1}):
        dim = (conf["k"]*img.shape[1], conf["k"]*img.shape[0])
        img_ = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        tesseract_bboxes = pytesseract.image_to_data(
            config=f"-l {conf['lang']} --psm {conf['psm']} --oem {conf['oem']}",
            image=img_,
            output_type=pytesseract.Output.DICT)
        word_list = []
        for index_bbox, level in enumerate(tesseract_bboxes["level"]):
            if level == 5:
                word_list.append({
                    "text": tesseract_bboxes["text"][index_bbox],
                    "x_top_left": round(tesseract_bboxes["left"][index_bbox]/conf["k"]),
                    "y_top_left": round(tesseract_bboxes["top"][index_bbox]/conf["k"]),
                    "width": round(tesseract_bboxes["width"][index_bbox]/conf["k"]),
                    "height": round(tesseract_bboxes["height"][index_bbox]/conf["k"]),
                })
        return word_list