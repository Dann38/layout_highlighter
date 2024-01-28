import pytesseract
import cv2
import base64
from img_doc.editors.binarizer import ValleyEmphasisBinarizer
from img_doc.extractors.word_extractors import BaseWordExtractor
from img_doc.extractors.word_extractors.word_bold_extractor import PsBoldExtractor, WidthBoldExtractor, ISPBoldExtractor
from img_doc.extractors.block_extractors.block_extractor_from_word import KMeanBlockExtractor
from img_doc.extractors.block_extractors.block_label_extractor import MLPExtractor, MLPAngLenExtractor, AngleLengthExtractor
from img_doc.data_structures import Word, Block
from img_doc.data_structures import Image, ImageSegment
import numpy as np
from typing import List
from io import StringIO
import json



class TesseractWordExtractor(BaseWordExtractor):
    def extract_from_img(self, img: np) -> List[Word]:
        tesseract_bboxes = pytesseract.image_to_data(
            config="-l eng+rus",
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
        self.BOLD_EXTRACTORS = {
            "isp": ISPBoldExtractor(),
            "width": WidthBoldExtractor(),
            "ps":PsBoldExtractor(),
        }
        self.LABEL_BLOCK_EXTRACTOR = {
            "mlp_len": MLPExtractor("/build/models/model-2.sav", {"len_vec": 5}),
            "mlp_len_big": MLPExtractor("/build/models/model-4.sav", {"len_vec": 5}),
            "mlp_len_big50": MLPExtractor("/build/models/model-5.sav", {"len_vec": 50}),
            "mlp_len_ang": MLPAngLenExtractor("/build/models/model-3.sav", {"len_vec": 5}),
            "mlp_len_ang_big50": MLPAngLenExtractor("/build/models/model-6.sav", {"len_vec": 50})
        }
        self.binarizer = ValleyEmphasisBinarizer()
        

    def segment2vec_distribution(self, image64, proc):
        _, _, words = self.get_segment_img_word_from_image64(image64, proc)
        rez = {
            "vec": self.LABEL_BLOCK_EXTRACTOR[proc["model_type"]].get_vec_from_words(words, proc["vec_len"]),
        }
        return rez

    def get_segment_from_image(self, image64, proc):
        _, segment_image, words = self.get_segment_img_word_from_image64(image64, proc)
        rez = {
            "image64": segment_image.get_base64().decode('utf-8'),
            "words": [word.to_dict() for word in words]
        }
        return rez
        
    def get_rez_proc(self, image64, proc):
        image = self.base64image(image64)

        history = dict()

        words = self.word_ext.extract_from_img(image.img)
        
        if ("bold" in proc) and ("bold_type" in proc):
            if proc["bold"]:
                gray_img = self.binarizer.binarize(image.img)
                self.BOLD_EXTRACTORS[proc["bold_type"]].extract(words, gray_img)
                gray_image = Image(cv2.cvtColor(gray_img*255, cv2.COLOR_GRAY2BGR))
                history["image64_binary"] = gray_image.get_base64().decode('utf-8')
        if "research_block" in proc and proc["research_block"]:
                dist_row = None
                dist_word = None
                model_type = None
                if "dist_row" in proc:
                    if proc["dist_row"] != "auto":
                        dist_row = proc["dist_row"]
                if "dist_word" in proc: 
                    if proc["dist_word"] != "auto":
                        dist_word = proc["dist_word"]
                if "model_type" in proc:
                    model_type = proc["model_type"]
                history["dist_word"] = 0
                history["dist_row"] = 0
                history["join_blocks"] = []
                history["no_join_blocks"] = []
                history["distans"] = []
                history["neighbors"] = []
                if len(words) > 1:
                    self.proccessing(dist_row, dist_word, history, words, model_type)
                elif len(words) == 1:
                    block = Block()
                    block.set_words(words)
                    history["no_join_blocks"] = [block]

                
                history["no_join_blocks"] = [block.to_dict() for block in history["no_join_blocks"]]
                history["join_blocks"] = [block.to_dict() for block in history["join_blocks"]]
            
        history["words"] = [word.to_dict() for word in words]
        return history
    
    def proccessing(self, dist_row, dist_word, history, words, model_type):
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
        if model_type is None:
            model_type = "mlp_len"
        self.LABEL_BLOCK_EXTRACTOR[model_type].extract(list_block)
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
    
    def get_segment_img_word_from_image64(self, image64, proc):
        image = self.base64image(image64)
        segment = ImageSegment(x_top_left=proc["x_top_left"],
                               y_top_left=proc["y_top_left"],
                               x_bottom_right=proc["x_bottom_right"],
                               y_bottom_right=proc["y_bottom_right"])
        segment_img = segment.get_segment_from_img(image.img)
        segment_image = Image(img=segment_img)

        is_into_segment = lambda point: (proc["x_top_left"] < point[0] and proc["x_bottom_right"] > point[0]and
                                         proc["y_top_left"] < point[1] and proc["y_bottom_right"] > point[1])
        
        words = self.word_ext.extract_from_img(image.img)
        words = [word for word in words if is_into_segment(word.segment.get_center())]
        return segment, segment_image, words
    
    def get_file_dataset(self, dataset, parametr):
        list_vec = []
        list_y = []
        vec_len = parametr["vec_len"]
        model_type = parametr["model_type"]
        is_into_segment = lambda point, json_seg: (json_seg["x_top_left"] < point[0] and json_seg["x_bottom_right"] > point[0] and
                                                   json_seg["y_top_left"] < point[1] and json_seg["y_bottom_right"] > point[1])
        for doc in dataset["documents"]:
            image = self.base64image(doc["image64"])
            words = self.word_ext.extract_from_img(image.img)

            list_seg = [seg for seg in dataset["segments"] if seg["document_id"] == doc["id"]]
            for seg in list_seg:
                seg_words = [word for word in words if is_into_segment(word.segment.get_center(), json.loads(seg["json_data"]))]
                list_vec.append(self.LABEL_BLOCK_EXTRACTOR[model_type].get_vec_from_words(seg_words, vec_len).tolist())
                list_y.append(seg["marking_id"])
        
        return {"x": list_vec, "y": list_y}
    
    def get_dir(self):
        import os
        return os.getcwd()
    