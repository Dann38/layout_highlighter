import base64

from fastapi import FastAPI

import uvicorn
import schemas
from typing import List

import tesseract_reader

app = FastAPI()
image_reader = tesseract_reader.ImageReader()


def run_api(host: str, port: int) -> None:
    uvicorn.run(app=app, host=host, port=port)


@app.post("/bboxes/", response_model=schemas.TesseractProcess)
async def read_images(base_64: schemas.TesseractProcess):
    img = image_reader.readb64(base_64.base64)
    conf = tesseract_reader.TesseractReaderConfig()
    t_reader = tesseract_reader.TesseractReader(conf)
    list_bboxes, base_64.list_text = t_reader.read(img)
    base_64.list_bboxes = [bbox.to_dict() for bbox in list_bboxes]
    return base_64
