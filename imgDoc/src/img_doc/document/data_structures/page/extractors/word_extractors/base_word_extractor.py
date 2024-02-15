from abc import ABC, abstractmethod


class BaseWordExtractor(ABC):
    @abstractmethod
    def extract(self, page: "Page", conf={}):
        pass