import unittest
from img_doc.document import Document, Page, Block
from img_doc.document.page.extractors.block_extractors import BLOCK_LABEL

class TestDocument(unittest.TestCase):
    def test_create_document(self):
        doc = Document()
        doc.set_from_path("file/1.jpg")
        self.assertEqual(type(doc.pages[0]), Page)

    def test_count_page_img(self):
        doc = Document()
        doc.set_from_path("file/1.jpg")
        self.assertEqual(len(doc.pages), 1)

    def test_count_page_pdf(self):
        doc = Document()
        doc.set_from_path("file/Rosenblatt1958.pdf")
        self.assertEqual(len(doc.pages), 23)

    def test_get_block(self):
        conf_old={
         "extractor_word":{
             "method":"tesseract",
             "conf": {"lang": "eng+rus", "psm": 4, "oem": 3, "k": 1},
         },
          "classification":{
              "type": "walk_rnd",
              "conf": {
                  "properties": ["many_dist", "many_angle", "place_in_block"], 
                  "count_step": 50,
                  "path_model": "../model_training/models/RWMDMAP-MP50/"}
          },
        }
        doc = Document()
        doc.set_from_path("file/1.jpg")
        block = doc.get_info_from_segment(num_page=0, x_top_left=100, y_top_left=170, 
                                  x_bottom_right=950, y_bottom_right=450, 
                                  conf=conf_old)
        self.assertEqual(type(block), Block)
        self.assertNotEqual(block.get_text(), "")
        self.assertIn(block.label, BLOCK_LABEL)


if __name__ == "__main__":
    unittest.main(verbosity=2)