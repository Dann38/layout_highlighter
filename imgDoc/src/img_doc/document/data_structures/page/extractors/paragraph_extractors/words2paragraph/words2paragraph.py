from ..base_paragraph_extractor import BaseParagraphExtractor
from img_doc.document.data_structures.page.data_structures.image import SetImageSegment
from img_doc.document.data_structures.page.data_structures.paragraph import Paragraph

class Words2Paragraph(BaseParagraphExtractor):
    def extract(self, page: "Page", conf={}):
        if "word_extractor" in conf.keys():
            conf_word_ext = conf["word_extractor"]
            page.extract_word(method=conf_word_ext["method"], conf=conf_word_ext["conf"])
        else:
            page.extract_word()

        set_segment = SetImageSegment([word.segment for word in page.words])
        set_segment.extract_parant_segment(method="kmean", conf={"dist_row": "auto", "dist_word": "auto"})

        page.paragraphs = []
        for pseg in set_segment.parent_segments:
            paragraph = Paragraph()
            paragraph.segment = pseg
            page.paragraphs.append(paragraph)

        for word in page.words:
            for paragraph in page.paragraphs:
                if paragraph.segment.is_intersection(word.segment):
                    paragraph.words.append(word)