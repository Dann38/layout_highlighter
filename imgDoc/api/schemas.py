from pydantic import BaseModel

class ImgAndSetProcess(BaseModel):
    image64: str
    process: str
    