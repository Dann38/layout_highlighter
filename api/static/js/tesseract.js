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
            functionResponseTesseract(response_tesseract);
            functionTesseractStep();
        }
    };
});

var functionResponseTesseract = function(response_tesseract){
    const bboxes = response_tesseract.list_bboxes;
    process.bboxes = bboxes;
    process.exist_data_step["tesseract"] = true;
}

var functionStartTesseractStep = function(){

}

var functionTesseractStep = function(){
    if (process.exist_data_step["tesseract"]){
        writeTesseract();
        unlockStep("graph");
    }
}

