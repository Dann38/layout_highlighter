from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.sql import null

import models, schemas
from typing import List


def create_document(db: Session, doc: schemas.CreateDocument) -> schemas.Document:
    db_document = models.Document(name=doc.name, image64=doc.image64)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    db_content = models.Content(document_id = db_document.id)
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    db_folder_content = models.FolderContent(content_id=db_content.id, 
                                             folder_parent_id=doc.folder_parent_id if doc.folder_parent_id != 0 else null())
    
    db.add(db_folder_content)
    db.commit()
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

# ------------------------------------------------------------------------------------------------------------
def create_folder(db: Session, folder: schemas.CreateFolder) -> schemas.Folder:
    db_folder = models.Folder(name = folder.name)
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)

    db_content = models.Content(folder_id = db_folder.id)
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    db_folder_content = models.FolderContent(content_id=db_content.id, 
                                             folder_parent_id=folder.folder_parent_id if folder.folder_parent_id != 0 else null())
    
    db.add(db_folder_content)
    db.commit()

    return schemas.Folder(id=db_folder.id,
                          name=db_folder.name, 
                          folders_id=[],
                          documents_id=[])


def delete_folder(db: Session, folder_id: int) -> bool:
    db_folder = db.query(models.Folder).get(folder_id)
    if db_folder:
        db.delete(db_folder)
        db.commit()
        return True
    return False


def move_folder(db: Session, folder_id: int, folder_parent_id) -> bool:
    db_content = db.query(models.Content).filter(models.Content.folder_id == folder_id).first()
    if folder_parent_id == 0:
        folder_parent_id = null()
    
    if not db_content:
        db_content = models.Content(folder_id=folder_id)
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        db_folder_content = models.FolderContent(folder_parent_id=folder_parent_id, content_id=db_content.id)
        db.add(db_folder_content)
    else: 
        db_content.folder_content[0].folder_parent_id = folder_parent_id
    db.commit()


def move_document(db: Session, doc_id: int, folder_parent_id) -> bool:
    db_content = db.query(models.Content).filter(models.Content.document_id == doc_id).first()
    if folder_parent_id == 0:
        folder_parent_id = null()

    if not db_content:
        db_content = models.Content(document_id=doc_id)
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        db_folder_content = models.FolderContent(folder_parent_id=folder_parent_id, content_id=db_content.id)
        db.add(db_folder_content)
    else: 
        db_content.folder_content[0].folder_parent_id = folder_parent_id
    db.commit()


def read_folder_content(db: Session, folder_id: int) -> schemas.Folder:
    if folder_id == 0:
        db_folder_content = db.query(models.FolderContent).filter(models.FolderContent.folder_parent_id == null()).all()
        doc_id = [fc.content.document_id for fc  in db_folder_content if fc .content.document_id is not None]
        folder_id = [fc.content.folder_id for fc in db_folder_content if fc .content.folder_id is not None]

        return schemas.Folder(id=0,
                            name="menu", 
                            folders_id=folder_id,
                            documents_id=doc_id)
    
    db_folder = db.query(models.Folder).get(folder_id)
    if db_folder:
        return schemas.Folder(id=db_folder.id,
                             name=db_folder.name, 
                             folders_id=[fc.content.folder_id for fc in db_folder.contents if fc .content.folder_id is not None],
                             documents_id=[fc.content.document_id for fc  in db_folder.contents if fc .content.document_id is not None])

   
    