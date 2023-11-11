import base64

from fastapi import Depends, FastAPI, UploadFile, File
from sqlalchemy.orm import Session
import uvicorn
import models, schemas, crud
from typing import List
from database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def run_api(host: str, port: int) -> None:
    uvicorn.run(app=app, host=host, port=port)


@app.post("/upload_image/")
async def create_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    print(file.filename)
    img = schemas.ImageCreate(bytes_img=contents)
    image = crud.create_image(db=db, image=img)
    # print(type(image.image), image.image)
    return image.id


@app.get("/images/")
async def read_images(page: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    images = crud.get_images(db, page=page, limit=limit)
    return [img.id for img in images]


@app.get("/image/{id_image}/")
async def read_image(id_image: str, db: Session = Depends(get_db)):
    images = crud.get_image_id(db, image_id=id_image)
    base64_utf8_str = base64.b64encode(images.image).decode('utf-8')
    return base64_utf8_str


@app.post("/processing_create/")
async def create_processing(proc: schemas.ProcessingCreate, db: Session = Depends(get_db)):
    processing = schemas.ProcessingCreate(id_image=proc.id_image)
    processing = crud.create_processing(db, processing)
    return processing.id


@app.get("/processing/{id_process}/")
async def read_processing(id_process: str, db: Session = Depends(get_db)):
    processing = crud.get_processing(db, id_process)
    return processing

