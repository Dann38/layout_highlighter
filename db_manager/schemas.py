from pydantic import BaseModel


class ImageBase(BaseModel):
    bytes_img: bytes


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    bytes_img: bytes
