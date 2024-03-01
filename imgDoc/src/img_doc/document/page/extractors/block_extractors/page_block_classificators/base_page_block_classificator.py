from abc import ABC, abstractmethod

"""
Гипотеза в том, что для классификации блока, кроме как информации о блока нужна информация о страницы
"""

class BasePageBlockClassificator(ABC):
    @abstractmethod
    def classification(self, page: "Page"):
        pass