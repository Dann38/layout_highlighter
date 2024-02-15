from abc import ABC, abstractmethod


class BaseParagraphExtractor(ABC):
    @abstractmethod
    def extract(self, page: "Page", conf={}):
        pass