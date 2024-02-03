from ..base_info import BaseInfo
from typing import List, Dict

class ListBlock(BaseInfo):
    def __init__(self, list_block: List[BaseInfo]) -> None:
        self.list_block = list_block

    def to_dict(self) -> List[Dict]:
        return [block.to_dict() for block in self.list_block]