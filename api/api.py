import json
import os

import requests
from flask import Flask, render_template, request


host_db_manager = "http://db_manager:1235"
host_img_doc = "http://doc_img:1238"

class File:
    def __init__(self):
        self.name = ""


app = Flask(__name__)
img = File()



@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/research/<int:doc_id>")
def research(doc_id: int):
    context = {
        "doc_id": doc_id
    }
    return render_template("research.html", context=context)

@app.route("/manual_marking/<int:doc_id>")
def manual_marking(doc_id: int):
    context = {
        "doc_id": doc_id
    }
    return render_template("manual_marking.html", context=context)

@app.route("/dataset/")
def dataset():
    return render_template("dataset_menu.html")

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

@app.route("/dataset/create/", methods=["POST"])
def dataset_create():
    discription = str(request.form["discription"])
    name = str(request.form["name"])
    content = requests.post(f'{host_db_manager}/dataset/create/', json={
        "discription": discription,
        "name": name}).content
    return content


@app.route("/dataset/read/")
def dataset_read():
    content = requests.get(f'{host_db_manager}/dataset/read/').content
    return content

@app.route("/dataset/delete/<int:dataset_id>", methods=["POST"])
def dataset_delete(dataset_id: int):
    content = requests.delete(f'{host_db_manager}/dataset/delete/{dataset_id}').content
    return content  

@app.route("/dataset/<int:dataset_id>/markingsegment/read/")
def marking_read(dataset_id: int):
    content = requests.get(f'{host_db_manager}/dataset/{dataset_id}/markingsegment/read/').content
    return content

@app.route("/markingsegment/delete/<int:marking_id>", methods=["POST"])
def marking_delete(marking_id: int):
    content = requests.delete(f"{host_db_manager}/markingsegment/delete/{marking_id}/").content
    return content

@app.route("/markingsegment/create/", methods=["POST"])
def marking_create():
    dataset_id = int(request.form["dataset_id"])
    name = str(request.form["name"])
    content = requests.post(f'{host_db_manager}/markingsegment/create/', json={
        "dataset_id": dataset_id,
        "name": name}).content
    return content