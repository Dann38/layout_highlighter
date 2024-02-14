from abc import ABC, abstractmethod
from img_doc.data_structures import Document

class BaseBlockExtractor(ABC):
    @abstractmethod
    def extract(self, doc: Document) -> None:
        pass
