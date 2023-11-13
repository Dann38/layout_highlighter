$("#a-indicator-tesseract").click(function(){
    if (!$("#a-indicator-tesseract")[0].classList.contains("link-secondary")) {
        $(".setting").css("display", "none");
        $("#tesseract-setting").css("display" ,"block");
        $("#indicator-tesseract").text("Текущий");
        $("#a-indicator-tesseract").removeClass("link-warning")
        $("#a-indicator-tesseract").addClass("link-primary");
    }
})

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
            for(var i = 0; i < bboxes.length; i++){
                const bbox = bboxes[i];
                writeRectangle(bbox.x_top_left, bbox.y_top_left, bbox.width, bbox.height);
            }
            changeIndicatorTesseract();
        }
    };
});


var changeIndicatorTesseract = function(){
    $("#a-indicator-tesseract").removeClass("link-primary");
    $("#a-indicator-tesseract").addClass("link-success");
    $("#indicator-tesseract").text("OK");
    $("#indicator-tesseract").removeClass("bg-primary");
    $("#indicator-tesseract").addClass("bg-success");
    $("#a-indicator-graph").removeClass("link-secondary");
    $("#a-indicator-graph").addClass("link-warning");
}
