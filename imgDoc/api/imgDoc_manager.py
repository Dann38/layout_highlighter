import pytesseract
import cv2
import base64
from img_doc.extractors.word_extractors import BaseWordExtractor
from img_doc.extractors.block_extractors.block_extractor_from_word import KMeanBlockExtractor
from img_doc.data_structures import Word
from img_doc.data_structures import Image
import numpy as np
from typing import List

class TesseractWordExtractor(BaseWordExtractor):
    def extract_from_img(self, img: np) -> List[Word]:
        tesseract_bboxes = pytesseract.image_to_data(
            config="-l rus",
            image=img,
            output_type=pytesseract.Output.DICT)
        word_list = []
        for index_bbox, level in enumerate(tesseract_bboxes["level"]):
            if level == 5:
                word = Word(text = tesseract_bboxes["text"][index_bbox])
                word.set_point_and_size({
                    "x_top_left":tesseract_bboxes["left"][index_bbox],
                    "y_top_left":tesseract_bboxes["top"][index_bbox],
                    "width":tesseract_bboxes["width"][index_bbox],
                    "height": tesseract_bboxes["height"][index_bbox],
                })
                word_list.append(word)
        return word_list
    
class ImgDocManager:
    def get_rez_proc(self, image64, proc):
        data = np.frombuffer(base64.b64decode(image64), np.uint8)
        image_np = cv2.imdecode(data, cv2.IMREAD_COLOR)
        image = Image(img=image_np)
        word_ext = TesseractWordExtractor()
        words = word_ext.extract_from_img(image.img)
        kmeanext = KMeanBlockExtractor()
        history = {"no_join_blocks":[], "dist_word": 0, "join_blocks": None,
        "neighbors": None, "distans": None}
        blocks = kmeanext.extract_from_word(words, history)
        history["words"] = [word.segment.get_segment_2p() for word in words]
        return history