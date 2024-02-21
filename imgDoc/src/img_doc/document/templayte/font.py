from typing import List, Dict
import numpy as np

class Char:
    def __init__(self) -> None:
        self.list_img: List[np.ndarray] = []



class Font:
    def __init__(self):
        self.width: float = None
        self.heigth: float = None
        self.alphabet: Dict[str, Char] = []


