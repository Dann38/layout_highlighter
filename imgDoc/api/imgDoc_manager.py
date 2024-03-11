import cv2
import base64
from img_doc.document import Document, Page, Block
from img_doc.image import Image, ImageSegment
from img_doc.extractors import LayoutExtractor
from typing import List
from io import StringIO
import json
import os

conf={
    "extractor_word":{
        "method":"tesseract",
        "conf": {"lang": "eng+rus", "psm": 4, "oem": 3, "k": 1},
    },
    "page_classification":{
        "type": "page_and_deep",
        "rnd_conf": {
            "properties":["many_dist", "many_angle", "place_in_block", "height", "bold"],
            "count_node":1, 
            "deep":2},
        "conf": {
            "properties":["place_in_page", "count_word_in_page"],
            "path_model": "/build/model_training/models/RDMDMAPHB-PLN/"
        }
    },
}

conf_new={
    "extractor_word":{
        "method":"tesseract",
        "conf": {"lang": "eng+rus", "psm": 4, "oem": 3, "k": 1},
    },
    "page_classification":{
        "type": "page_and_walk",
        "rnd_conf": {
            "properties":["hist_ang", "hist_bold", "hist_dist", "hist_height"],
            "count_step":0},
        "conf": {
            "properties":["place_in_page", "count_word_in_page"],
            "path_model": "/build/model_training/models/Hdabh-PLN/"
        }
    },
}


class ImgDocManager:
    def __init__(self) -> None:
        self.layaout_ext = LayoutExtractor()

    # def segment2vec_distribution(self, image64, proc):
    #     _, _, words = self.get_segment_img_word_from_image64(image64, proc)
    #     model_type = proc["model_type"]
    #     model_version = proc["model_version"]
    #     model = self.LABEL_BLOCK_EXTRACTOR_CLASS[model_type](self.LABEL_BLOCK_EXTRACTOR_CONFIG[model_type][model_version])
    #     rez = {
    #         "vec": model.get_vec_from_words(words, proc["vec_len"]),
    #     }
    #     return rez

    # def get_segment_from_image(self, image64, proc):
    #     _, segment_image, words = self.get_segment_img_word_from_image64(image64, proc)
    #     rez = {
    #         "image64": segment_image.get_base64().decode('utf-8'),
    #         "words": [word.to_dict() for word in words]
    #     }
    #     return rez
        
    def get_rez_proc(self, image64, proc):
        image = Image()
        image.set_base64(image64)
        page = Page()
        doc = Document()
        page.image = image
        page.set_from_np(page.image.img)
        doc.pages = [page]

        history = dict()
        
        # if ("bold" in proc) and ("bold_type" in proc):
        #     if proc["bold"]:
        #         words = self.word_ext.extract_from_img(image.img)
        #         gray_img = self.binarizer.binarize(image.img)
        #         self.BOLD_EXTRACTORS[proc["bold_type"]].extract(words, gray_img)
        #         gray_image = Image(cv2.cvtColor(gray_img*255, cv2.COLOR_GRAY2BGR))
        #         history["image64_binary"] = gray_image.get_base64().decode('utf-8')
        #         history["words"] = [word.to_dict() for word in words]

        if "research_block" in proc and proc["research_block"]:
                self.layaout_ext.extract(doc)
                doc.pages[0].blocks = []
                doc.pages[0].extract_word_bold()
                for paragraph in doc.pages[0].paragraphs:
                    block = Block(paragraph.segment.get_segment_2p())
                    block.words = paragraph.words
                    doc.pages[0].blocks.append(block)
                
                doc.pages[0].classification_block(conf_new["page_classification"])
                dict_page = doc.pages[0].to_dict()
                history["join_blocks"] = dict_page["blocks"]
                history["words"] = dict_page["words"]
                      
        return history
    
    # def get_segment_img_word_from_image64(self, image64, proc):
    #     image = Image()
    #     image.set_base64(image64)
    #     segment = ImageSegment(x_top_left=proc["x_top_left"],
    #                            y_top_left=proc["y_top_left"],
    #                            x_bottom_right=proc["x_bottom_right"],
    #                            y_bottom_right=proc["y_bottom_right"])
    #     segment_img = segment.get_segment_from_img(image.img)
    #     segment_image = Image(img=segment_img)

    #     is_into_segment = lambda point: (proc["x_top_left"] < point[0] and proc["x_bottom_right"] > point[0]and
    #                                      proc["y_top_left"] < point[1] and proc["y_bottom_right"] > point[1])
        
    #     words = self.word_ext.extract_from_img(image.img)
    #     words = [word for word in words if is_into_segment(word.segment.get_center())]
    #     return segment, segment_image, words
    
    # def get_file_dataset(self, dataset, parametr, fun_get_image):
    #     list_vec = []
    #     list_y = []
    #     vec_len = parametr["vec_len"]
    #     model_type = parametr["model_type"]
    #     conf = self.pass_config_model
    #     conf["vec_len"] = vec_len 
    #     model = self.LABEL_BLOCK_EXTRACTOR_CLASS[model_type](conf)
    #     is_into_segment = lambda point, json_seg: (json_seg["x_top_left"] < point[0] and json_seg["x_bottom_right"] > point[0] and
    #                                                json_seg["y_top_left"] < point[1] and json_seg["y_bottom_right"] > point[1])
    #     for doc in dataset["documents"]:
    #         image = fun_get_image(doc["image64"])
    #         words = self.word_ext.extract_from_img(image.img)

    #         list_seg = [seg for seg in dataset["segments"] if seg["document_id"] == doc["id"]]
    #         for seg in list_seg:
    #             seg_words = [word for word in words if is_into_segment(word.segment.get_center(), json.loads(seg["json_data"]))]
    #             np_vec = model.get_vec_from_words(seg_words, vec_len)
    #             list_vec.append(np_vec.tolist())
    #             list_y.append(seg["marking_id"])
        
    #     return {"x": list_vec, "y": list_y}

    # def get_dataset_from_db(self, dataset, parametr):
    #     def fun_get_image(ib64):
    #         image = Image()
    #         image.set_base64(ib64)
    #         return image
    #     return self.get_file_dataset(dataset, parametr, fun_get_image)

    # def get_dataset_from_dir(self, path_dir, balans = 1000):
    #     # Этот путь нужно указать в функции чтения fun_get_image
    #     train_images = os.path.join(path_dir, "train")
    #     with open(os.path.join(path_dir, "train.json"), "r") as f:
    #         train_json = json.load(f)
    #     dataset = dict()
    #     dataset["documents"] = [{"image64": img["file_name"], "id": img["id"]} for img in train_json["images"]]
    #     dataset["segments"] = []
    #     list_count_category = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    #     for seg in train_json["annotations"]:
    #         if list_count_category[seg["category_id"]] < balans:
    #             dataset["segments"].append({"json_data": "{"+f'"x_top_left":{int(seg["bbox"][0])}, "y_top_left":{int(seg["bbox"][1])}, "x_bottom_right": {int(seg["bbox"][0]+seg["bbox"][2])}, "y_bottom_right": {int(seg["bbox"][1]+seg["bbox"][3])}'+"}",
    #                             "marking_id": seg["category_id"],
    #                             "document_id": seg["image_id"]
    #                            })
    #             list_count_category[seg["category_id"]] += 1
 
    #     return dataset