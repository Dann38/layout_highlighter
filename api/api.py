import json
import os

import requests
from flask import Flask, render_template, request


host_db_manager = "http://db_manager:1235"
host_tesseract = "http://tesseract:1236"
host_graph = "http://graph:1237"
host_img_doc = "http://doc_img:1238"

class File:
    def __init__(self):
        self.name = ""


app = Flask(__name__)
img = File()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu/")
def menu():
    return render_template("menu.html")

@app.route("/research/<int:doc_id>")
def research(doc_id: int):
    context = {
        "doc_id": doc_id
    }
    return render_template("research.html", context=context)




@app.route("/doc/read/")
def doc_read():
    content = requests.get(f'{host_db_manager}/doc/read/').content
    return content

@app.route("/doc/read/<int:doc_id>")
def doc_read_one(doc_id: int):
    content = requests.get(f'{host_db_manager}/doc/read/{doc_id}').content
    return content

@app.route("/doc/create/", methods=["POST"])
def doc_create():
    image = str(request.form["file"])
    name = str(request.form["name"])
    content = requests.post(f'{host_db_manager}/doc/create/', json={
        "image64": image,
        "name": name}).content
    return content

@app.route("/doc/delete/<int:doc_id>")
def doc_delete(doc_id: int):
    content = requests.delete(f'{host_db_manager}/doc/delete/{doc_id}').content
    return content    



@app.route("/doc/research/", methods=["POST"])
def doc_research():
    doc_id = int(request.form["doc_id"])
    proc_set = str(request.form["proc_set"])
    rez = requests.get(f'{host_db_manager}/doc/read/{doc_id}').json()
    
    image = rez["image64"]
    content = requests.post(f'{host_img_doc}/processing/', json={
        "image64": image,
        "process": proc_set}).content
    return content



@app.route("/proc/read/")
def proc_read():
    content = requests.get(f'{host_db_manager}/proc/read/').content
    return content

@app.route("/proc/read/<int:proc_id>")
def proc_read_one(proc_id: int):
    content = requests.get(f'{host_db_manager}/proc/read/{proc_id}').content
    return content

@app.route("/proc/create/", methods=["POST"])
def proc_create():
    json_processing = str(request.form["json_processing"])
    name = str(request.form["name"])
    content = requests.post(f'{host_db_manager}/proc/create/', json={
        "json_processing": json_processing,
        "name": name}).content
    return content

@app.route("/proc/delete/<int:proc_id>")
def proc_delete(proc_id: int):
    content = requests.delete(f'{host_db_manager}/proc/delete/{proc_id}').content
    return content  














@app.route("/upload_image", methods=["POST"])
def upload():
    requests_upload = requests.post(f'{host_db_manager}/upload_image', files=request.files)
    return requests_upload.content


@app.route("/image/<id_image>", methods=["GET"])
def get_image(id_image: str):
    requests_upload = requests.get(f'{host_db_manager}/image/{id_image}', files=request.files)
    return requests_upload.content


@app.route("/get_processes", methods=["GET"])
def get_processes():
    content = requests.get(f'{host_db_manager}/processes/?page=1&limit=10').content
    return content


@app.route("/get_history", methods=["GET"])
def get_history():
    content = requests.get(f'{host_db_manager}/images/?page=1&limit=10').content
    return content
#
#
# @app.route("/get_set_classifier/<int:id_image>", methods=["GET"])
# def get_set_classifier(id_image):
#     content = requests.get(f'{host_classifier}/file/get_set_classifier/{id_image}').content
#     return json.loads(content)


@app.route("/processing_create/<id_image>", methods=["POST"])
def create_processing(id_image: str):
    content = requests.post(f'{host_db_manager}/processing_create/', json={"id_image": id_image}).content
    return content


@app.route("/tesseract_process/", methods=["POST"])
def tesseract_processing():
    id_process = str(request.form["id_process"])
    id_image = requests.get(f'{host_db_manager}/processing/{id_process}').json()["id_image"]
    image = bytes.decode(get_image(id_image=id_image), "utf-8")

    content = requests.post(f'{host_tesseract}/bboxes/', json={
        "base64": image,
        "list_bboxes": [
                {}
        ],
        "list_text": [
             "string"
        ]}).content
    return content


@app.route("/graph_process/", methods=["POST"])
def point_processing():
    bboxes = json.loads(request.form["bboxes"])
    count = int(request.form["count"])
    point_rez = json.loads(requests.post(f'{host_graph}/bboxes_to_points/', json={
        "list_bboxes": bboxes,
        "count": count
    }).text)
    points = point_rez["list_point"]
    bboxes_edge = point_rez["bboxes_edge"]
    edges = json.loads(requests.post(f'{host_graph}/point_to_delone/', json={
        "list_point": points
    }).text)["list_edge"]

    return {"list_point": points, "list_edge": edges, "bboxes_edge": bboxes_edge}


@app.route("/width_segments/", methods=["POST"])
def width_segments():
    edges = json.loads(request.form["edges"])
    points = json.loads(request.form["points"])
    threshold = float(request.form["threshold"])

    mandatory_links = json.loads(request.form["mandatory_links"])

    content = requests.post(f'{host_graph}/width_segments/', json={
        "list_edge": edges,
        "list_point": points,
        "threshold": threshold,
        "mandatory_links": mandatory_links,
    }).content
    return content


@app.route("/manual_segments/", methods=["POST"])
def manual_segments():
    edges = json.loads(request.form["edges"])
    points = json.loads(request.form["points"])
    delete_edges = json.loads(request.form["delete_edges"])
    mandatory_links = json.loads(request.form["mandatory_links"])

    content = requests.post(f'{host_graph}/manual_segments/', json={
        "list_edge": edges,
        "list_point": points,
        "delete_edges": delete_edges,
        "mandatory_links": mandatory_links,
    }).content
    return content


@app.route("/get_labels", methods=["GET"])
def get_labels():
    content = requests.get(f'{host_db_manager}/labels/').content
    return content


@app.route("/create_label", methods=["POST"])
def create_label():
    name = str(request.form["name"])
    content = requests.post(f'{host_db_manager}/label_create/', json={"name": name}).content
    return content
