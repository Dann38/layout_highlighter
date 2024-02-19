from .base_dataset_extractor import BaseDatasetDocExtractor
import json
from time import time


def dataset2json(path_json:str, path_dataset:str, ds_ext: BaseDatasetDocExtractor, fun_doc2vecs,  is_only_segment:bool = True):
    start = time()
    
    docs = ds_ext.dataset_extractor(path_dataset)
    
    finish_read_dataset_time = time()

    x_array = []
    y_array = []
    coef_proc = 100/len(docs)
    if is_only_segment:
        for i, doc in enumerate(docs):
            print(f"{i*coef_proc:.2f}%"+" "*10, end="\r")
            try:
                x, y = fun_doc2vecs(doc)
                for xi, yi in zip(x, y):
                    x_array.append(xi)
                    y_array.append(yi)
            except:
                print("ERROR:", doc.path)
    else:
        for i, doc in enumerate(docs):
            try:
                print(f"{i*coef_proc:.2f}%"+" "*10, end="\r")
                x, y = fun_doc2vecs(doc)
                x_array.append(x)
                y_array.append(y)
            except:
                print("ERROR:", doc.path)

    finish_create_vec = time()

    with open(path_json, "w") as f:
        json.dump({"x": x_array, "y": y_array}, f)
    
    finish_save_file = time()
    print(f"open dataset: {finish_read_dataset_time-start:.0f} sec.")
    print(f"create dataset: {finish_create_vec-finish_read_dataset_time:.0f} sec.")
    print(f"save json: {finish_save_file-finish_create_vec:.0f} sec.")

