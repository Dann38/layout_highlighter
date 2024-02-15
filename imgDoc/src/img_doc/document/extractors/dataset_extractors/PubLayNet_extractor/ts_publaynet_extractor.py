from typing import List
from img_doc.document.data_structures import Word, Page
from .publaynet_extractor import PubLayNetExtractor
import json

class TsPubLayNetExtractor(PubLayNetExtractor):
    def extract(self, doc: "Document") -> None:
        path_json = doc.path + ".json"
        with open(path_json, "r") as f:
            rez = json.load(f)
        words = []
        for w in rez["words"]:
            word = Word(w)
            words.append(word)
        doc.pages[0].words = words
        for word in doc.pages[0].words:
            for block in doc.pages[0].blocks:
                if block.segment.is_intersection(word.segment):
                    block.words.append(word)