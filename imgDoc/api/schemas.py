from pydantic import BaseModel

class ImgAndSetProcess(BaseModel):
    image64: str
    process: str


class DatasetAndParametr(BaseModel):
    parametr: str
    dataset: str