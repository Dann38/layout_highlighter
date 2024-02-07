
import cv2
import base64
from img_doc.editors.binarizer import ValleyEmphasisBinarizer
from img_doc.extractors.word_extractors.word_extractor_from_img import TesseractWordExtractor

from img_doc.extractors.word_extractors.word_bold_extractor import *
from img_doc.extractors.block_extractors.block_extractor_from_word import KMeanBlockExtractor
from img_doc.extractors.block_extractors.block_label_extractor import *
from img_doc.data_structures import Word, Block
from img_doc.data_structures import Image, ImageSegment
from img_doc.extractors.page_extractors.page_extractors_from_img import W2BExtractor
from typing import List
from io import StringIO
import json
import os


class ImgDocManager:
    def __init__(self):
        self.word_ext = TesseractWordExtractor()
        self.kmeanext = KMeanBlockExtractor()
        self.page_ext = W2BExtractor()
        self.BOLD_EXTRACTORS = {
            "ps":PsBoldExtractor(),
            "textps": TextPsBoldExtractor(),
        }

        self.LABEL_BLOCK_EXTRACTOR_CLASS = {
            "mlp_len": MLPExtractor,
            "mlp_len_ang": MLPAngLenExtractor,
            "rnd_walk_dist": MLPRandomWalkExtractor,
            "rnd_walk_many_dist": MLPRandomWalkExtractor,
        }
        self.pass_config_model =  {"model_file": "/build/models/mlp_len-micro_5.sav", "len_vec": 5}
        self.LABEL_BLOCK_EXTRACTOR_CONFIG= {
            "mlp_len": {
                "micro_5": {"model_file": "/build/models/mlp_len-micro_5.sav", "len_vec": 5},
                "mini_publaynet_5": {"model_file": "/build/models/mlp_len-mini_publaynet_5.sav", "len_vec": 5},
                "mini_publaynet_50": {"model_file": "/build/models/mlp_len-mini_publaynet_50.sav", "len_vec": 50},
            },
            "mlp_len_ang":{
                "micro_5": {"model_file": "/build/models/mlp_len_ang-micro_5.sav", "len_vec": 5},
                "mini_publaynet_50": {"model_file": "/build/models/mlp_len_ang-mini_publaynet_50.sav", "len_vec": 50},
            },
            "rnd_walk_dist":{
                "micro_50": {"model_file": "/build/models/mlp_rnd_walk_dist-micro_50.sav", "len_vec": 50},
                "mini_publaynet_50": {"model_file": "/build/models/mlp_rnd_walk_dist-mini_publaynet_50.sav", "len_vec": 50},
                "micro_publaynet_50": {"model_file": "/build/models/mlp_rnd_walk_dist-micro_publaynet_50.sav", "len_vec": 50}
            },
            "rnd_walk_many_dist":{
                "mini_publaynet_50": {"model_file": "/build/models/mlp_rnd_walk_many_dist-mini_publaynet_50.sav", "len_vec": 200},
            }
        }
        
        
        self.binarizer = ValleyEmphasisBinarizer()
        

    def segment2vec_distribution(self, image64, proc):
        _, _, words = self.get_segment_img_word_from_image64(image64, proc)
        model_type = proc["model_type"]
        model_version = proc["model_version"]
        model = self.LABEL_BLOCK_EXTRACTOR_CLASS[model_type](self.LABEL_BLOCK_EXTRACTOR_CONFIG[model_type][model_version])
        rez = {
            "vec": model.get_vec_from_words(words, proc["vec_len"]),
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
        image = Image()
        image.set_base64(image64)

        history = dict()
        
        if ("bold" in proc) and ("bold_type" in proc):
            if proc["bold"]:
                words = self.word_ext.extract_from_img(image.img)
                gray_img = self.binarizer.binarize(image.img)
                self.BOLD_EXTRACTORS[proc["bold_type"]].extract(words, gray_img)
                gray_image = Image(cv2.cvtColor(gray_img*255, cv2.COLOR_GRAY2BGR))
                history["image64_binary"] = gray_image.get_base64().decode('utf-8')
                history["words"] = [word.to_dict() for word in words]

        if "research_block" in proc and proc["research_block"]:
                
                model_type = proc["model_type"] if "model_type" in proc else "mlp_len"
                model_version = proc["model_version"] if "model_version" in proc else "micro_5"

                self.page_ext.block_label_ext = self.LABEL_BLOCK_EXTRACTOR_CLASS[model_type](self.LABEL_BLOCK_EXTRACTOR_CONFIG[model_type][model_version])
        
                self.page_ext.save_no_join_blocks = True
                self.page_ext.save_neighbors = True
                self.page_ext.save_distans = True

                self.page_ext.set_dist_row = proc["dist_row"] if "dist_row" in proc else None 
                self.page_ext.set_dist_word = proc["dist_word"] if "dist_word" in proc else None 
                page = self.page_ext.extract_from_image(image)
                page_info = page.to_dict()
                for key, item in page_info.items():
                    history[key] = item       
        return history
    
    def get_segment_img_word_from_image64(self, image64, proc):
        image = Image()
        image.set_base64(image64)
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
    
    def get_file_dataset(self, dataset, parametr, fun_get_image):
        list_vec = []
        list_y = []
        vec_len = parametr["vec_len"]
        model_type = parametr["model_type"]
        conf = self.pass_config_model
        conf["vec_len"] = vec_len 
        model = self.LABEL_BLOCK_EXTRACTOR_CLASS[model_type](conf)
        is_into_segment = lambda point, json_seg: (json_seg["x_top_left"] < point[0] and json_seg["x_bottom_right"] > point[0] and
                                                   json_seg["y_top_left"] < point[1] and json_seg["y_bottom_right"] > point[1])
        for doc in dataset["documents"]:
            image = fun_get_image(doc["image64"])
            words = self.word_ext.extract_from_img(image.img)

            list_seg = [seg for seg in dataset["segments"] if seg["document_id"] == doc["id"]]
            for seg in list_seg:
                seg_words = [word for word in words if is_into_segment(word.segment.get_center(), json.loads(seg["json_data"]))]
                np_vec = model.get_vec_from_words(seg_words, vec_len)
                list_vec.append(np_vec.tolist())
                list_y.append(seg["marking_id"])
        
        return {"x": list_vec, "y": list_y}

    def get_dataset_from_db(self, dataset, parametr):
        def fun_get_image(ib64):
            image = Image()
            image.set_base64(ib64)
            return image
        return self.get_file_dataset(dataset, parametr, fun_get_image)

    def get_dataset_from_dir(self, path_dir, balans = 1000):
        # Этот путь нужно указать в функции чтения fun_get_image
        train_images = os.path.join(path_dir, "train")
        with open(os.path.join(path_dir, "train.json"), "r") as f:
            train_json = json.load(f)
        dataset = dict()
        dataset["documents"] = [{"image64": img["file_name"], "id": img["id"]} for img in train_json["images"]]
        dataset["segments"] = []
        list_count_category = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for seg in train_json["annotations"]:
            if list_count_category[seg["category_id"]] < balans:
                dataset["segments"].append({"json_data": "{"+f'"x_top_left":{int(seg["bbox"][0])}, "y_top_left":{int(seg["bbox"][1])}, "x_bottom_right": {int(seg["bbox"][0]+seg["bbox"][2])}, "y_bottom_right": {int(seg["bbox"][1]+seg["bbox"][3])}'+"}",
                                "marking_id": seg["category_id"],
                                "document_id": seg["image_id"]
                               })
                list_count_category[seg["category_id"]] += 1
 
        return dataset