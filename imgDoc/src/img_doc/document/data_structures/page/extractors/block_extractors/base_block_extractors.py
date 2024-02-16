from abc import ABC, abstractmethod

class BaseBlockExtractors(ABC):
    def extract(self, page: "Page"):
        pass