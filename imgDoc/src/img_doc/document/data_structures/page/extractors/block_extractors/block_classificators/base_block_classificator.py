from abc import ABC, abstractmethod
from img_doc.document.data_structures.page.data_structures import Block

"""
Гипотеза в том, что для классификации блока, кроме как информации о блока ничего не нужно
"""

class BaseBlockClassificator(ABC):
    @abstractmethod
    def classification(self, block: Block):
        pass