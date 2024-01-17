import base64

from fastapi import Depends, FastAPI, UploadFile, File
from sqlalchemy.orm import Session
import uvicorn
import models, schemas, crud
from typing import List, Dict
from database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def run_api(host: str, port: int) -> None:
    uvicorn.run(app=app, host=host, port=port)

# -----------------------------------------------------------------------------------------------------------

@app.post("/doc/create/")
async def create_document(doc: schemas.CreateDocument, db: Session = Depends(get_db)) -> schemas.Document:
    doc = crud.create_document(db=db, doc=doc)
    return doc

@app.delete("/doc/delete/{doc_id}/")
async def delete_document(doc_id: int, db: Session = Depends(get_db)) -> bool:
    is_delete = crud.delete_document(db=db, doc_id=doc_id)
    return is_delete

@app.get("/doc/read/{doc_id}/")
async def read_document(doc_id: int, db: Session = Depends(get_db)) -> schemas.Document:
    doc = crud.read_document(db=db, doc_id=doc_id)
    return doc   

@app.get("/doc/read/")
async def read_documents(db: Session = Depends(get_db)) -> List[schemas.Document]:
    docs= crud.read_documents(db=db)
    return docs   

# -----------------------------------------------------------------------------------------------------------

@app.post("/proc/create/")
async def create_processing(proc: schemas.CreateProcessing, db: Session = Depends(get_db)) -> schemas.Processing:
    proc = crud.create_processing(db=db, proc=proc)
    return proc

@app.delete("/proc/delete/{proc_id}/")
async def delete_processing(proc_id: int, db: Session = Depends(get_db)) -> bool:
    is_delete = crud.delete_processing(db=db, proc_id=proc_id)
    return is_delete

@app.get("/proc/read/{proc_id}/")
async def read_processing(proc_id: int, db: Session = Depends(get_db)) -> schemas.Processing:
    proc = crud.read_processing(db=db, proc_id=proc_id)
    return proc   

@app.get("/proc/read/")
async def read_processings(db: Session = Depends(get_db)) -> List[schemas.Processing]:
    procs= crud.read_processings(db=db)
    return procs   

# -----------------------------------------------------------------------------------------------------------

@app.post("/dataset/create/")
async def create_dataset(dataset: schemas.CreateDataset, db: Session = Depends(get_db)) -> schemas.Dataset:
    dataset = crud.create_dataset(db=db, dataset=dataset)
    return dataset

@app.delete("/dataset/delete/{dataset_id}/")
async def delete_dataset(dataset_id: int, db: Session = Depends(get_db)) -> bool:
    is_delete = crud.delete_dataset(db=db, dataset_id=dataset_id)
    return is_delete

@app.get("/dataset/read/{dataset_id}/")
async def read_dataset(dataset_id: int, db: Session = Depends(get_db)) -> schemas.Dataset:
    dataset = crud.read_dataset(db=db, dataset_id=dataset_id)
    return dataset   

@app.get("/dataset/read/")
async def read_datasets(db: Session = Depends(get_db)) -> List[schemas.Dataset]:
    datasets= crud.read_datasets(db=db)
    return datasets  

# -----------------------------------------------------------------------------------------------------------

@app.post("/markingsegment/create/")
async def create_marking(mark: schemas.CreateMarkingSegment, db: Session = Depends(get_db)) -> schemas.MarkingSegment:
    mark = crud.create_marking(db=db, mark=mark)
    return mark

@app.delete("/markingsegment/delete/{mark_id}/")
async def delete_marking(mark_id: int, db: Session = Depends(get_db)) -> bool:
    is_delete = crud.delete_marking(db=db, mark_id=mark_id)
    return is_delete

@app.get("/markingsegment/read/{mark_id}/")
async def read_marking(mark_id: int, db: Session = Depends(get_db)) -> schemas.MarkingSegment:
    mark = crud.read_marking(db=db, mark_id=mark_id)
    return mark   

@app.get("/dataset/{dataset_id}/markingsegment/read/")
async def read_markings(dataset_id: int, db: Session = Depends(get_db)) -> List[schemas.MarkingSegment]:
    marks= crud.read_markings(db=db, dataset_id=dataset_id)
    return marks  

# -----------------------------------------------------------------------------------------------------------

@app.post("/segmentdata/create/")
async def create_segment_data(sd: schemas.CreateSegmentData, db: Session = Depends(get_db)) -> schemas.SegmentData:
    sd = crud.create_segment_data(db=db, sd=sd)
    return sd

@app.delete("/segmentdata/delete/{sd_id}/")
async def delete_marking(sd_id: int, db: Session = Depends(get_db)) -> bool:
    is_delete = crud.delete_segment_data(db=db, sd_id=sd_id)
    return is_delete

@app.get("/segmentdata/read/{sd_id}/")
async def read_segment_data(sd_id: int, db: Session = Depends(get_db)) -> schemas.SegmentData:
    sd = crud.read_segment_data(db=db, sd_id=sd_id)
    return sd   

@app.get("/dataset/{dataset_id}/segmentdata/read/")
async def read_dataset_segment_datas(dataset_id: int, db: Session = Depends(get_db)) -> List[schemas.SegmentData]:
    sds= crud.read_dataset_segment_datas(db=db, dataset_id=dataset_id)
    return sds  

@app.get("/doc/{doc_id}/segmentdata/read/")
async def read_document_segment_datas(doc_id: int, db: Session = Depends(get_db)) -> List[schemas.SegmentData]:
    sds= crud.read_document_segment_datas(db=db, doc_id=doc_id)
    return sds  

@app.get("/markingsegment/{mark_id}/segmentdata/read/")
async def read_marking_segment_datas(mark_id: int, db: Session = Depends(get_db)) -> List[schemas.SegmentData]:
    sds= crud.read_marking_segment_datas(db=db, mark_id=mark_id)
    return sds