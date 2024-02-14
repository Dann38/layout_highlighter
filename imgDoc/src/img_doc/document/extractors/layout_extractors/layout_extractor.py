from img_doc import Document

class LayoutExtractor:
    def extract(self, doc:Document) -> None:
        for page in doc.pages:
            page.extract_paragraphs()
