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


def get_processes(db: Session, page: int = 1, limit: int = 10) -> List[schemas.Processing]:
    skip = (1 - page) * limit
    rez = db.query(models.Processing).order_by(desc(models.Processing.date_update)).offset(skip).limit(limit).all()
    return [schemas.Processing(id=str(r.id), id_image=str(r.id_image)) for r in rez]


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


def create_document(db: Session, doc: schemas.CreateDocument) -> schemas.Document:
    db_document = models.Document(name=doc.name, image64=doc.image64)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return schemas.Document(id=db_document.id,
                            name=db_document.name,
                            image64=db_document.image64 )


def read_document(db: Session, doc_id: int) -> schemas.Document:
    db_document = db.query(models.Document).get(doc_id)
    return schemas.Document(id=db_document.id,
                            name=db_document.name,
                            image64=db_document.image64 )

def read_documents(db: Session) -> List[schemas.Document]:
    docs = db.query(models.Document).all()
    return [schemas.Document(id=db_document.id,
                            name=db_document.name,
                            image64=db_document.image64 ) for db_document in docs]


def delete_document(db: Session, doc_id: int) -> bool:
    db_document = db.query(models.Document).get(doc_id)
    if db_document:
        db.delete(db_document)
        db.commit()
        return True
    return False

