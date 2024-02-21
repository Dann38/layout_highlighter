from img_doc.document import Document

class LayoutExtractor:
    def extract(self, doc:Document) -> None:
        for page in doc.pages:
            page.extract_paragraphs()
