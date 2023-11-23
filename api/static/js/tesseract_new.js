var tesseract = {};
tesseract.data = {};

tesseract.setting = function(proc){
}

tesseract.post = function(res, proc){
    proc.bboxes = res.list_bboxes;
}

tesseract.run = function(proc){
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    const id_process = proc.id;
    formData.append('id_process', id_process);

    xhr.open('POST', '/tesseract_process');
    xhr.send(formData);

    xhr.onload = function() {
        if (xhr.status != 200) {
          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            var res = $.parseJSON(xhr.response);
            tesseract.post(res, proc);
            tesseract.write_res(proc);
            unlockStep("graph");
        }
    };
}

tesseract.write_res = function(proc){
    for(var i = 0; i < proc.bboxes.length; i++){
        const bbox = proc.bboxes[i];
        writeRectangle(bbox.x_top_left, bbox.y_top_left, bbox.width, bbox.height);
    }
}

tesseract.init = function(proc){
    select("tesseract");
}