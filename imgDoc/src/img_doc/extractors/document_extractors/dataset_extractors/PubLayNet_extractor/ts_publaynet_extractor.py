from typing import List
from img_doc.data_structures import Document, Word, Page
from .publaynet_extractor import PubLayNetExtractor
import json

class TsPubLayNetExtractor(PubLayNetExtractor):
    def extract(self, doc: Document) -> None:
        path_json = doc.path + ".json"
        with open(path_json, "r") as f:
            rez = json.load(f)
        words = []
        for w in rez["words"]:
            word = Word()
            word.set_two_points(w)
            words.append(word)
        page = Page()
        page.words = words
        doc.pages.append(page)