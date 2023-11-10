from pydantic import BaseModel
from typing import List, Dict


class TesseractProcess(BaseModel):
    base64: str
    list_bboxes: List[Dict]
    list_text: List[str]

