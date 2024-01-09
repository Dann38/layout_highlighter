import numpy as np
from img_doc.data_structures import Word
from abc import ABC, abstractmethod
from typing import List


class BaseWordExtractor(ABC):
    @abstractmethod
    def extract_from_img(self, img: np.ndarray) -> List[Word]:
        pass



