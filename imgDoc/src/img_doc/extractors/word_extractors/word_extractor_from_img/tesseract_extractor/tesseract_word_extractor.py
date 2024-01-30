import pytesseract
from img_doc.extractors.word_extractors import BaseWordExtractor
import numpy as np
from typing import List
from img_doc.data_structures import Word

class TesseractWordExtractor(BaseWordExtractor):
    def extract_from_img(self, img: np) -> List[Word]:
        tesseract_bboxes = pytesseract.image_to_data(
            config="-l eng+rus --psm 4 --oem 3",
            image=img,
            output_type=pytesseract.Output.DICT)
        word_list = []
        for index_bbox, level in enumerate(tesseract_bboxes["level"]):
            if level == 5:
                word = Word(text = tesseract_bboxes["text"][index_bbox])
                word.set_point_and_size({
                    "x_top_left": tesseract_bboxes["left"][index_bbox],
                    "y_top_left": tesseract_bboxes["top"][index_bbox],
                    "width": tesseract_bboxes["width"][index_bbox],
                    "height": tesseract_bboxes["height"][index_bbox],
                })
                word_list.append(word)
        return word_list