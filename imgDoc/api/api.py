from fastapi import FastAPI
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
    process = img_and_set_process.process
    rez = img_doc_manager.get_rez_proc(image64, process)
    rez["no_join_blocks"] = [block.segment.get_segment_2p() for block in rez["no_join_blocks"]]
    rez["join_blocks"] = [block.segment.get_segment_2p() for block in rez["join_blocks"]]
    
    
    return json.dumps(rez)