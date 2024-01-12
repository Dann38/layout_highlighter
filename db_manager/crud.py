from sqlalchemy.orm import Session
from sqlalchemy import desc

import models, schemas
from typing import List


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


def create_processing(db: Session, proc: schemas.CreateProcessing) -> schemas.Processing:
    db_processing = models.Processing(name=proc.name, json_processing=proc.json_processing)
    db.add(db_processing)
    db.commit()
    db.refresh(db_processing)
    return schemas.Processing(id=db_processing.id,
                            name=db_processing.name,
                            json_processing=db_processing.json_processing )


def read_processing(db: Session, proc_id: int) -> schemas.Processing:
    db_processing = db.query(models.Processing).get(proc_id)
    return schemas.Processing(id=db_processing.id,
                            name=db_processing.name,
                            json_processing=db_processing.json_processing )

def read_processings(db: Session) -> List[schemas.Processing]:
    procs = db.query(models.Processing).all()
    return [schemas.Processing(id=db_processing.id,
                            name=db_processing.name,
                            json_processing=db_processing.json_processing ) for db_processing in procs]


def delete_processing(db: Session, proc_id: int) -> bool:
    db_processing = db.query(models.Processing).get(proc_id)
    if db_processing:
        db.delete(db_processing)
        db.commit()
        return True
    return False
