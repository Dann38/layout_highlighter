from typing import List
# from img_doc.data_structures import Document, Templayte, ImageSegment, SegmentInformation
from ..base_dataset_extractor import BaseDatasetDocExtractor
import os
import json

class PubLayNetExtractor(BaseDatasetDocExtractor):
    def extract(self, doc: "Document") -> None:
        pass
    
    def dataset_extractor(self, path_dataset) -> List["Document"]:
        # images_path = os.path.join(path_dataset, "train")
        # with open(os.path.join(path_dataset, "train.json"), "r") as f:
        #     train_json = json.load(f)
        # docs_dict = dict()
        # for img in train_json["images"]:
        #     doc = Document()
        #     doc.templates.append(Templayte())
        #     doc.path =  os.path.join(images_path, img["file_name"])
        #     docs_dict[img["id"]] = doc
        # for seg in train_json["annotations"]:
        #     seg_ = ImageSegment()
        #     seg_.set_segment_p_size({"x_top_left":int(seg["bbox"][0]), "y_top_left":int(seg["bbox"][1]),
        #                              "width": int(seg["bbox"][2]), "height":int(seg["bbox"][3])})
        #     seg_info = SegmentInformation(seg_, {"marking_id": seg["category_id"]})
        #     docs_dict[seg["image_id"]].templates[0].segments.append(seg_info)
        
        # docs = [doc for _, doc in docs_dict.items()]
        # for doc in docs:
        #     self.extract(doc)
        # return docs
        pass