from fastapi import FastAPI

import uvicorn
import schemas
from typing import List


app = FastAPI()


def run_api(host: str, port: int) -> None:
    uvicorn.run(app=app, host=host, port=port)


@app.post("/bboxes_to_points/")
async def read_images(bboxes: schemas.CreatePointBboxes) -> schemas.Point:
    points_list = []
    if bboxes.count == 1:
        for bbox in bboxes.list_bboxes:
            y = round(bbox["y_top_left"] + bbox["height"] / 2)
            x = round(bbox["x_top_left"] + bbox["width"] / 2)
            points_list.append({"x": x, "y": y})
    return schemas.Point(list_point=points_list)

