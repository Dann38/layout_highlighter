from abc import ABC, abstractmethod

"""
Гипотеза в том, что для классификации блока, кроме как информации о блока ничего не нужно
"""

BLOCK_LABEL = ["no_struct", "text", "header",  "list", "table"]

class BaseBlockClassificator(ABC):
    @abstractmethod
    def classification(self, block: "Block"):
        pass