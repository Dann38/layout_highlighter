from abc import ABC, abstractmethod

class BaseBlockExtractors(ABC):
    @abstractmethod
    def extract(self, page: "Page"):
        pass