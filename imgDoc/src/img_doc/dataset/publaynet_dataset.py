import os
import json
from typing import List


# Номер символа, с которого начинается информация о картинках, аннотации, категориях
IMAGE_START = 1 
ANNOTATION_START = 27417937 
CATEGORY_START = 1696001803

STEP_ANNOTATION = 1000
STEP_IMAGE = 300

LABEL_PUBLAYNET2IMGDOC = {
    1:1, # text - text
    2:2, # title - header
    3:3, # list - list
    4:4, # table - table
    5:0, # figure -no_struct
}

class PubLayNetDataset:
    def __init__(self, path_dataset, tmp_path_dataset = None) -> None:
        self.path_dataset = path_dataset
        self.path_json_train = os.path.join(self.path_dataset, "train.json")
        self.path_dir_train_image = os.path.join(self.path_dataset, "train")
        
        if tmp_path_dataset:
            self.tmp_path_dataset = tmp_path_dataset
            self.tmp_path_train_jsons = os.path.join(self.tmp_path_dataset, "train")
        


    def __json_step_read(self, path_json:str, seek:int=0, step:int=2000) -> str:
        with open(path_json, "r") as f:
            f.seek(seek)
            str_ = f.read(step)
        return str_
    
    def create_tmp_annotation_jsons(self, path_tmp_dataset, fun_additional_info, start_min_category=0, finish_min_category=100):
        self.tmp_path_dataset = path_tmp_dataset
        self.tmp_path_train_jsons = os.path.join(self.tmp_path_dataset, "train")
        if not os.path.exists(self.tmp_path_dataset):
            os.mkdir(self.tmp_path_dataset)
            os.mkdir(self.tmp_path_train_jsons)

        self.__create_tmp_train_annotation_jsons(fun_additional_info, start_min_category, finish_min_category)

    def __create_tmp_train_annotation_jsons(self, fun_additional_info, start_min_category, finish_min_category):
        # TODO добавить время
        annotation_image = self.__get_annotation_train_json(start_min_category, finish_min_category)
        images = self.__get_image_train_json(annotation_image.keys())
        images_len = len(images)
        print(f"кол-во изображений:\t {len(annotation_image)}")
       

        for i, img in enumerate(images):
            pr = i/images_len*100
            print(f"    {pr:.2f}%    ", end="\r" )
            img_path = os.path.join(self.path_dir_train_image, img["file_name"])
            additional_info = fun_additional_info(img_path)
            blocks = [{"x_top_left":int(aimg["bbox"][0]), 
                       "y_top_left":int(aimg["bbox"][1]),
                       "width": int(aimg["bbox"][2]), 
                       "height":int(aimg["bbox"][3]),
                       "label": LABEL_PUBLAYNET2IMGDOC[aimg["category_id"]]
                      }for aimg in annotation_image[img["id"]]]
            with open(os.path.join(self.tmp_path_train_jsons, img["file_name"]+".json"), 'w') as f:
                json.dump({"blocks": blocks, "additional_info": additional_info}, f)

    def __get_annotation_train_json(self, start_min_category, finish_min_category):
        key_category = '"category_id"'
        key_image_id = '"image_id"'
        len_key_category = 3+len(key_category)
        list_count_category = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        annotation_image = dict()
        seek = ANNOTATION_START
        start_ = False
        while seek < CATEGORY_START:    
            str_ = self.__json_step_read(self.path_json_train, seek=seek, step=STEP_ANNOTATION)
            index_char_category = str_.find(key_category)
            rigth_border = seek+index_char_category+len_key_category
            if index_char_category != -1:
                str_info = self.__json_step_read(self.path_json_train, seek=rigth_border-STEP_ANNOTATION, step=STEP_ANNOTATION)
                index_char_image = str_info.rfind(key_image_id)
                rez = json.loads("{" + str_info[index_char_image:] + "}")
                

                list_count_category[rez["category_id"]] += 1
                
                if start_:
                    if rez["image_id"] in annotation_image.keys():
                        annotation_image[rez["image_id"]].append(rez) 
                    else:
                        annotation_image[rez["image_id"]] = [rez]
                
                min_count = min([c for _, c in list_count_category.items()])
                if not start_ and min_count >= start_min_category:
                    start_ = True
                elif min_count >= finish_min_category:
                    break

    
            seek = rigth_border  
        return annotation_image
    
    def __get_image_train_json(self, image_ids: List[int]):
        key_filename = '"file_name"'
        list_exit = dict()
        for key in image_ids:
            list_exit[key] = False
            
        images = []
        seek = IMAGE_START
        while seek < ANNOTATION_START:    
            str_ = self.__json_step_read(self.path_json_train, seek=seek, step=STEP_IMAGE)
            index_char_filename = str_.find(key_filename)
            left_border = seek+index_char_filename-1
            if index_char_filename != -1:
                str_info = self.__json_step_read(self.path_json_train, left_border, step=STEP_IMAGE)
                right_bord = str_info.find("}")
                rez = json.loads(str_info[:right_bord+1])
                if rez["id"] in list_exit.keys():
                    if not list_exit[rez["id"]]: 
                        list_exit[rez["id"]] = True
                        images.append(rez)
                for key, ind in list_exit.items():
                    if ind:
                        break
            seek = left_border+right_bord 

        return images
    
    def get_json_from_tmps_and_images(self, fun_from_tmp_and_path_image):
        train = self.__get_json_from_train_tmps_and_images(fun_from_tmp_and_path_image)

        return {"train": train}
    
    def __get_json_from_train_tmps_and_images(self, fun_from_tmp_and_path_image):
        list_tmp_jsons = os.listdir(self.tmp_path_train_jsons)
        rez = []
        a = 1/len(list_tmp_jsons)
        print("train:")
        for i, name_tmp_json in enumerate(list_tmp_jsons):
            pr = a*i*100
            print(f"    {pr:.2f}%    ", end="\r" )
            path_tmp_json =os.path.join(self.tmp_path_train_jsons, name_tmp_json)
            with open(path_tmp_json, "r") as f:
                tmp_json = json.load(f)
            path_image = os.path.join(self.path_dir_train_image, name_tmp_json[:-5])
            rez.append(fun_from_tmp_and_path_image(tmp_json, path_image))
        return rez

