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

#------------------------------------------------------------------------------------------------------------

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

# ------------------------------------------------------------------------------------------------------------

def create_dataset(db: Session, dataset: schemas.CreateDataset) -> schemas.Dataset:
    db_dataset = models.Dataset(name=dataset.name, discription=dataset.discription)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return schemas.Dataset(id=db_dataset.id,
                            name=db_dataset.name,
                            discription=db_dataset.discription)


def read_dataset(db: Session, dataset_id: int) -> schemas.Dataset:
    db_dataset = db.query(models.Dataset).get(dataset_id)
    return schemas.Dataset(id=db_dataset.id,
                            name=db_dataset.name,
                            discription=db_dataset.discription)

def read_datasets(db: Session) -> List[schemas.Dataset]:
    db_datasets = db.query(models.Dataset).all()
    return [schemas.Dataset(id=db_dataset.id,
                            name=db_dataset.name,
                            discription=db_dataset.discription) for db_dataset in db_datasets]


def delete_dataset(db: Session, dataset_id: int) -> bool:
    db_dataset = db.query(models.Dataset).get(dataset_id)
    if db_dataset:
        db.delete(db_dataset)
        db.commit()
        return True
    return False


# ------------------------------------------------------------------------------------------------------------
def create_marking(db: Session, mark: schemas.CreateMarkingSegment) -> schemas.MarkingSegment:
    db_mark = models.MarkingSegment(name=mark.name, dataset_id=mark.dataset_id)
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return schemas.MarkingSegment(id=db_mark.id,
                                 name=db_mark.name,
                                 dataset_id=db_mark.dataset_id)


def read_marking(db: Session, mark_id: int) -> schemas.MarkingSegment:
    db_mark = db.query(models.MarkingSegment).get(mark_id)
    return schemas.MarkingSegment(id=db_mark.id,
                                 name=db_mark.name,
                                 dataset_id=db_mark.dataset_id)

def read_markings(db: Session, dataset_id: int) -> List[schemas.MarkingSegment]:
    db_datasets = db.query(models.Dataset).get(dataset_id)
    if db_datasets:
        return [schemas.MarkingSegment(id=db_mark.id,
                                      name=db_mark.name,
                                      dataset_id=db_mark.dataset_id) for db_mark in db_datasets.markings]


def delete_marking(db: Session, mark_id: int) -> bool:
    db_mark = db.query(models.MarkingSegment).get(mark_id)
    if db_mark:
        db.delete(db_mark)
        db.commit()
        return True
    return False

# ------------------------------------------------------------------------------------------------------------
def create_segment_data(db: Session, sd: schemas.CreateSegmentData) -> schemas.SegmentData:
    db_sd = models.SegmentData(document_id=sd.document_id, marking_id=sd.marking_id, json_data=sd.json_data)
    db.add(db_sd)
    db.commit()
    db.refresh(db_sd)
    return schemas.SegmentData(id=db_sd.id,
                               document_id=db_sd.document_id,
                               marking_id=db_sd.marking_id,
                               json_data=db_sd.json_data)


def read_segment_data(db: Session, sd_id: int) -> schemas.SegmentData:
    db_sd = db.query(models.SegmentData).get(sd_id)
    return schemas.SegmentData(id=db_sd.id,
                               document_id=db_sd.document_id,
                               marking_id=db_sd.marking_id,
                               json_data=db_sd.json_data)



def read_document_segment_datas(db: Session, doc_id: int) -> List[schemas.SegmentData]:
    db_doc = db.query(models.Document).get(doc_id)
    if db_doc:
        return [schemas.SegmentData(id=db_sd.id,
                                    document_id=db_sd.document_id,
                                    marking_id=db_sd.marking_id,
                                    json_data=db_sd.json_data) for db_sd in db_doc.segment_data]
    

def read_marking_segment_datas(db: Session, mark_id: int) -> List[schemas.SegmentData]:
    db_mark = db.query(models.MarkingSegment).get(mark_id)
    if db_mark:
        return [schemas.SegmentData(id=db_sd.id,
                                    document_id=db_sd.document_id,
                                    marking_id=db_sd.marking_id,
                                    json_data=db_sd.json_data) for db_sd in db_mark.segment_data]
    

def read_dataset_segment_datas(db: Session, dataset_id: int) -> List[schemas.SegmentData]:
    db_dataset = db.query(models.Dataset).get(dataset_id)
    if not db_dataset:
        return 
    
    marks = [m.id for m in db_dataset.markings]
    db_sds = db.query(models.SegmentData).filter(models.SegmentData.marking_id.in_(marks)).all()
    if db_sds:
        return [schemas.SegmentData(id=db_sd.id,
                                    document_id=db_sd.document_id,
                                    marking_id=db_sd.marking_id,
                                    json_data=db_sd.json_data) for db_sd in db_sds]


def delete_segment_data(db: Session, sd_id: int) -> bool:
    db_sd = db.query(models.SegmentData).get(sd_id)
    if db_sd:
        db.delete(db_sd)
        db.commit()
        return True
    return False
