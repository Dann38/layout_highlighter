from img_doc.data_structures import Page, Image
from abc import ABC, abstractmethod



class BasePageExtractor(ABC):
    @abstractmethod
    def extract_from_image(self, image: Image) -> Page:
        pass



