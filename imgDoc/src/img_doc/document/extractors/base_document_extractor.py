from img_doc.data_structures import Document

from abc import ABC, abstractmethod

class BaseDocumentExtractor(ABC):
    @abstractmethod
    def extract(self, doc: Document) -> None:
        pass

