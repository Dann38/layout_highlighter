from fastapi import FastAPI, Response
from imgDoc_manager import ImgDocManager
import json
import uvicorn
import schemas


app = FastAPI()
img_doc_manager = ImgDocManager()
def run_api(host: str, port: int) -> None:
    uvicorn.run(app=app, host=host, port=port)


@app.post("/processing/")
async def read_images(img_and_set_process: schemas.ImgAndSetProcess):
    image64 = img_and_set_process.image64
    process = json.loads(img_and_set_process.process)
    rez = img_doc_manager.get_rez_proc(image64, process)
    return json.dumps(rez)


@app.post("/segment_from_image/")
async def segment_from_image(img_and_set_process: schemas.ImgAndSetProcess):
    image64 = img_and_set_process.image64
    process = json.loads(img_and_set_process.process)
    rez = img_doc_manager.get_segment_from_image(image64, process)
    return json.dumps(rez)


@app.post("/segment2vec/distribution/")
async def segment2vec_distribution(img_and_set_process: schemas.ImgAndSetProcess):
    image64 = img_and_set_process.image64
    process = json.loads(img_and_set_process.process)
    rez = img_doc_manager.segment2vec_distribution(image64, process)
    return json.dumps(rez)


@app.post("/create_dataset/")
async def segment2vec_distribution(dataset_and_parametr: schemas.DatasetAndParametr):
    dataset = json.loads(dataset_and_parametr.dataset)
    parametr = json.loads(dataset_and_parametr.parametr)
    rez = img_doc_manager.get_file_dataset(dataset, parametr, img_doc_manager.base64image)
    return json.dumps(rez)
