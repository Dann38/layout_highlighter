$("#button_open_processing").click(
    function(){
        $("#button_open_processing").text("Новое исследование");
        $("#progress").css("display" ,"block");
        $("#upload-setting").css("display" ,"block");
        $("#history-list").css("display" ,"block");
        addHistory();
    }
);

$("#start_processing").click(function(){
    changeIndicatorImage();
    const get_processing = new XMLHttpRequest();
    const id_image = $("#image-id")[0].dataset["rowId"];
    console.log(id_image);
    get_processing.open('POST', '/processing_create/' + id_image);
    get_processing.send();

    get_processing.onload = function() {
        console.log(get_processing.response);
        console.log($.parseJSON(get_processing.response));
        $("#progress").attr("data-row-id", $.parseJSON(get_processing.response));
    }

})

var changeIndicatorImage = function(){
    $("#a-indicator-image").removeClass("link-primary");
    $("#a-indicator-image").addClass("link-success");
    $("#indicator-image").text("OK");
    $("#indicator-image").removeClass("bg-primary");
    $("#indicator-image").addClass("bg-success");
    $("#a-indicator-tesseract").removeClass("link-secondary");
    $("#a-indicator-tesseract").addClass("link-warning");
}