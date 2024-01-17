import pytesseract
import cv2
import base64
from img_doc.extractors.word_extractors import BaseWordExtractor
from img_doc.extractors.block_extractors.block_extractor_from_word import KMeanBlockExtractor
from img_doc.extractors.block_extractors.block_label_extractor import AngleLengthExtractor
from img_doc.data_structures import Word, Block
from img_doc.data_structures import Image, ImageSegment
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
                    "x_top_left": tesseract_bboxes["left"][index_bbox],
                    "y_top_left": tesseract_bboxes["top"][index_bbox],
                    "width": tesseract_bboxes["width"][index_bbox],
                    "height": tesseract_bboxes["height"][index_bbox],
                })
                word_list.append(word)
        return word_list


class ImgDocManager:
    def __init__(self):
        self.word_ext = TesseractWordExtractor()
        self.kmeanext = KMeanBlockExtractor()
        self.classifier = AngleLengthExtractor()

    def get_segment_from_image(self, image64, proc):
        image = self.base64image(image64)
        segment = ImageSegment(x_top_left=proc["x_top_left"],
                               y_top_left=proc["y_top_left"],
                               x_bottom_right=proc["x_bottom_right"],
                               y_bottom_right=proc["y_bottom_right"])
        segment_img = segment.get_segment_from_img(image.img)
        segment_image = Image(img=segment_img)
        rez = {
            "image64": segment_image.get_base64().decode('utf-8')
        }
        return rez

    def get_rez_proc(self, image64, proc):
        image = self.base64image(image64)

        history = {"no_join_blocks": [], "dist_word": 0, "dist_row": 0, "join_blocks": None,
        "neighbors": None, "distans": None}

        dist_row = None
        dist_word = None
        if "dist_row" in proc:
            if proc["dist_row"] != "auto":
                dist_row = proc["dist_row"]
        if "dist_word" in proc: 
            if proc["dist_word"] != "auto":
                dist_word = proc["dist_word"]
        
        words = self.word_ext.extract_from_img(image.img)
        self.proccessing(dist_row, dist_word, history, words)

        if "save_words" in proc:
            if proc["save_words"] == True:
                history["words"] = [word.segment.get_segment_2p() for word in words]
        history["no_join_blocks"] = [block.to_dict() for block in history["no_join_blocks"]]
        history["join_blocks"] = [block.to_dict() for block in history["join_blocks"]]
           
        if "save_blocks" in proc:
            if proc["save_blocks"] == False:
                del history["no_join_blocks"]
                del history["join_blocks"]
        return history
    
    def proccessing(self, dist_row, dist_word, history, words):
        neighbors = self.kmeanext.get_index_neighbors_word(words)
        distans = self.kmeanext.get_distans(neighbors, words)
        dist_word_, dist_row_ = self.kmeanext.get_standart_distant(distans)
        if dist_row is None:
            dist_row = dist_row_
        if dist_word is None:
            dist_word = dist_word_

        graph = self.kmeanext.get_graph_words(words, neighbors, dist_word, dist_row, distans)
        blocks = self.kmeanext.extract_from_word(words, history)
        
        list_block = []
        for r in graph.get_related_graphs():
            block = Block()
            words_r = [words[n.index-1] for n in r.get_nodes()]
            block.set_words(words_r)
            list_block.append(block)

        self.classifier.extract(list_block)
        join_intersect_block = self.kmeanext.join_intersect_blocks(list_block)

        if "join_blocks" in history.keys():
            history["join_blocks"] = join_intersect_block
        if "neighbors" in history.keys():
            history["neighbors"] = neighbors
        if "distans" in history.keys():
            history["distans"] = distans
        if "dist_word" in history.keys():
            history["dist_word"] = dist_word
        if "dist_row" in history.keys():
            history["dist_row"] = dist_row
        if "graph" in history.keys():
            history["graph"] = graph
        if "no_join_blocks" in history.keys():
            history["no_join_blocks"] = list_block

    def base64image(self, image64) -> Image:
        data = np.frombuffer(base64.b64decode(image64), np.uint8)
        image_np = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return Image(img=image_np)