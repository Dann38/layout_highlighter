from typing import List
from img_doc.document import Document
from img_doc.document.data_structures import Page
from img_doc.document.data_structures.page.data_structures import Block, ImageSegment
from ..base_dataset_extractor import BaseDatasetDocExtractor
import os
import json

LABEL_PUBLAYNET2IMGDOC = {
    1:1, # text - text
    2:2, # title - header
    3:3, # list - list
    4:4, # table - table
    5:0, # figure -no_struct
}


class PubLayNetExtractor(BaseDatasetDocExtractor):
    def extract(self, doc: "Document") -> None:
        pass
    
    def dataset_extractor(self, path_dataset) -> List["Document"]:
        images_path = os.path.join(path_dataset, "train")
        with open(os.path.join(path_dataset, "train.json"), "r") as f:
            train_json = json.load(f)
        docs_dict = dict()
        for img in train_json["images"]:
            doc = Document()
            doc.path =  os.path.join(images_path, img["file_name"])
            doc.pages.append(Page())
            docs_dict[img["id"]] = doc
        for seg in train_json["annotations"]:
            seg_ = ImageSegment()
            seg_.set_segment_p_size({"x_top_left":int(seg["bbox"][0]), "y_top_left":int(seg["bbox"][1]),
                                     "width": int(seg["bbox"][2]), "height":int(seg["bbox"][3])})
            
            block = Block()
            block.segment=seg_
            block.label = LABEL_PUBLAYNET2IMGDOC[seg["category_id"]]
            docs_dict[seg["image_id"]].pages[0].blocks.append(block)
        
        docs = [doc for _, doc in docs_dict.items()]
        for doc in docs:
            self.extract(doc)
        return docs
        pass