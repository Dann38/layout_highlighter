$("#button_tesseract").click(function(){

    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    const id_process = process.id;
    formData.append('id_process', id_process);

    xhr.open('POST', '/tesseract_process');
    xhr.send(formData);

    xhr.onload = function() {
        if (xhr.status != 200) {
          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            var response_tesseract = $.parseJSON(xhr.response);
            const bboxes = response_tesseract.list_bboxes;
            process.bboxes = bboxes;
            process.exist_data_step["tesseract"] = true;
            functionTesseractStep();
        }
    };
});

var functionStartTesseractStep = function(){}

var functionTesseractStep = function(){
    if (process.exist_data_step["tesseract"]){
        functionImageStep();
        for(var i = 0; i < process.bboxes.length; i++){
            const bbox = process.bboxes[i];
            writeRectangle(bbox.x_top_left, bbox.y_top_left, bbox.width, bbox.height);
        }
        unlockStep("graph");
    }
}

