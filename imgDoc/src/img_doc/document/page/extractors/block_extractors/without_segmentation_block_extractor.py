from .base_block_extractors import BaseBlockExtractors
"""
Гипотеза в том, что можно сначало выделить блоки, а потом работать с ними, т.е.
вся информация необходимая для определения положения блока известна, 
и то что определяется здесь никак не связано с его положением.
(гипотеза очень наивная, но на практике может работать хорошо).
"""


class WithoutSegmentationBlockExtractor(BaseBlockExtractors):
    def __init__(self, classifer):
        self.classifer = classifer
        

    def extract(self, page: "Page"):
        for block in page.blocks:
            self.classifer(block)
            # Может быть еще что-то, например,
            # повторное считывание слов зная вид блока 
            # (таблицы имеют особую структуру, списки имеют итераторы или маркеры и т.д.)