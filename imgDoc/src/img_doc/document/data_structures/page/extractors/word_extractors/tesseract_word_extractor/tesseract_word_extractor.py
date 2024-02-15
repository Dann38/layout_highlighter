import pytesseract
from ..base_word_extractor import BaseWordExtractor
import numpy as np
from typing import List

class TesseractWordExtractor(BaseWordExtractor):
    def extract(self, page: "Page", conf={}):
        if not conf:
            conf = {"lang": "eng+rus", "psm": 4, "oem": 3}
        tesseract_bboxes = pytesseract.image_to_data(
            config=f"-l {conf['lang']} --psm {conf['psm']} --oem {conf['oem']}",
            image=page.image.img,
            output_type=pytesseract.Output.DICT)
        word_list = []
        for index_bbox, level in enumerate(tesseract_bboxes["level"]):
            if level == 5:
                word_list.append({
                    "text": tesseract_bboxes["text"][index_bbox],
                    "x_top_left": tesseract_bboxes["left"][index_bbox],
                    "y_top_left": tesseract_bboxes["top"][index_bbox],
                    "width": tesseract_bboxes["width"][index_bbox],
                    "height": tesseract_bboxes["height"][index_bbox],
                })
        page.set_words_from_dict(word_list)
