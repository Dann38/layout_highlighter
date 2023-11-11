from pydantic import BaseModel


class ImageBase(BaseModel):
    bytes_img: bytes


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: str
    bytes_img: bytes


class ProcessingBase(BaseModel):
    id_image: str


class ProcessingCreate(ProcessingBase):
    pass


class Processing(ProcessingBase):
    id: str
