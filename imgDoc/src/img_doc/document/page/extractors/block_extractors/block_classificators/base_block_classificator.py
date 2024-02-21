from abc import ABC, abstractmethod
from img_doc.document.page import Block

"""
Гипотеза в том, что для классификации блока, кроме как информации о блока ничего не нужно
"""

class BaseBlockClassificator(ABC):
    @abstractmethod
    def classification(self, block: Block):
        pass