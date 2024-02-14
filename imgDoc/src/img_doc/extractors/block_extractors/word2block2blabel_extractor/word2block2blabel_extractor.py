from ..base_block_extractor import BaseBlockExtractor
from img_doc.data_structures import Document

from img_doc.extractors.word_extractors import BaseWordExtractor, TesseractWordExtractor
from img_doc.extractors.block_extractors.block_extractor_from_word import BaseBlockExtractorFromWord, KMeanBlockExtractor
from img_doc.extractors.block_extractors.block_label_extractor import BaseBlockLabelExtractor

class Word2Block2BlockLabelExtractor(BaseBlockExtractor):
    def __init__(self, 
                 blabel_ext: BaseBlockLabelExtractor, 
                 block_ext: BaseBlockExtractorFromWord = KMeanBlockExtractor(), 
                 word_ext: BaseWordExtractor = TesseractWordExtractor()) -> None:
        self.word_ext = word_ext
        self.block_ext = block_ext
        self.blabel_ext = blabel_ext


    def extract(self, doc: Document) -> None:
        for page in doc.pages:
            page.words = self.word_ext.extract_from_img(page.image.img)
            page.blocks = self.block_ext.extract_from_word(page.words)
            self.blabel_ext.extract(page.blocks)