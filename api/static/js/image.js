$("#button_open_processing").click(
    function(){
        $("#button_open_processing").text("Новое исследование");
        $("#progress").css("display" ,"block");
        select("image");
    }
);

$("#start_processing").click(function(){
    const get_processing = new XMLHttpRequest();
    const id_image = process.id_image;
    get_processing.open('POST', '/processing_create/' + id_image);
    get_processing.send();

    get_processing.onload = function() {
        process.id = $.parseJSON(get_processing.response);
    }
    unlockStep("tesseract");
})


var openImage = function(id_image){
    const get_img = new XMLHttpRequest();

    get_img.open('GET', '/image/' + id_image);
    get_img.send();

    get_img.onload = function() {
        process.image_base64 = $.parseJSON(get_img.response);
        process.id_image = id_image;
        process.exist_data_step["image"] = true;
        functionImageStep();
    }
}

var functionStartImageStep = function() {
    $("#history-list").css("display" ,"block");
    addHistory();
}

var functionImageStep = function(){
    if (process.exist_data_step["image"]){
        writeImage(process.image_base64);
    }
}

