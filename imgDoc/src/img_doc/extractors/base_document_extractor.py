from abc import ABC, abstractmethod

class BaseDocumentExtractor(ABC):
    @abstractmethod
    def extract(self, doc: "Document") -> None:
        pass

