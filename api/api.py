import json
import os

import requests
from flask import Flask, render_template, request


host_db_manager = "http://db_manager:1235"
host_tesseract = "http://tesseract:1236"


class File:
    def __init__(self):
        self.name = ""


app = Flask(__name__)
img = File()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload_image", methods=["POST"])
def upload():
    # bytes_file = request.files["file"].stream.read()
    requests_upload = requests.post(f'{host_db_manager}/upload_image', files=request.files)
    # print(requests_upload)
    # id_image = json.loads(requests_upload.content)["id_image"]

    return requests_upload.content


@app.route("/image/<id_image>", methods=["GET"])
def get_image(id_image: str):
    requests_upload = requests.get(f'{host_db_manager}/image/{id_image}', files=request.files)
    return requests_upload.content


# @app.route("/classify_image/<int:id_image>", methods=["POST"])
# def classifier(id_image):
#     method = int(request.form["method_classifier"])
#     coef = float(request.form["coef"])
#     requests.post(f'{host_classifier}/file/classify/{id_image}', json={"method": method, "coef": coef})
#     return {}
#
#
# @app.route("/get_image_result/<int:id_image>", methods=["GET"])
# def get_image_result(id_image):
#     return requests.get(f'{host_classifier}/file/get_result/{id_image}').content
#
#
# @app.route("/get_image_origin/<int:id_image>", methods=["GET"])
# def get_image_origin(id_image):
#     return requests.get(f'{host_classifier}/file/get_origin/{id_image}').content
#
#
@app.route("/get_history", methods=["GET"])
def get_history():
    content = requests.get(f'{host_db_manager}/images/?page=0&limit=10').content
    return content
#
#
# @app.route("/get_set_classifier/<int:id_image>", methods=["GET"])
# def get_set_classifier(id_image):
#     content = requests.get(f'{host_classifier}/file/get_set_classifier/{id_image}').content
#     return json.loads(content)
