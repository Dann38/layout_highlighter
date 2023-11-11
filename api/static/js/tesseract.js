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
    const id_process = $("#progress")[0].dataset["rowId"];
    formData.append('id_process', id_process);

    xhr.open('POST', '/tesseract_process');
    xhr.send(formData);

    xhr.onload = function() {
        if (xhr.status != 200) {
          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            var response_tesseract = $.parseJSON(xhr.response);
            console.log(response_tesseract)
        }
    };
});
