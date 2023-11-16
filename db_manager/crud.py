from sqlalchemy.orm import Session
from sqlalchemy import desc

import models, schemas
from typing import List


def get_image_id(db: Session, image_id: str):
    rez = db.query(models.Image).filter(models.Image.id == image_id).first()
    return rez


def create_image(db: Session, image: schemas.ImageCreate):
    db_image = models.Image(image=image.bytes_img)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_images(db: Session, page: int = 1, limit: int = 10):
    skip = (1-page)*limit
    rez = db.query(models.Image).order_by(desc(models.Image.date_create)).offset(skip).limit(limit).all()
    return rez


def create_processing(db: Session, processing: schemas.ProcessingCreate) -> schemas.Processing:
    db_processing = models.Processing(id_image=processing.id_image)
    db.add(db_processing)
    db.commit()
    db.refresh(db_processing)
    return db_processing


def get_processing(db: Session, processing_id: str) -> schemas.Processing:
    rez = db.query(models.Processing).filter(models.Processing.id == processing_id).first()
    return rez


def get_label(db: Session, label_id: int) -> schemas.Label:
    rez = db.query(models.Label).filter(models.Label.id == label_id).first()
    return schemas.Label(id=rez[0], name=rez[1])


def get_labels(db: Session) -> List[schemas.Label]:
    rez = db.query(models.Label).all()
    return rez


def create_label(db: Session, label: schemas.LabelCreate) -> schemas.Label:
    db_label = models.Label(name=label.name)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return schemas.Label(id=db_label.id, name=db_label.name)
