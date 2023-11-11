var addHistoryImg = function(id, pr=false) {

    var card = document.createElement('div');
    card.classList.add("card");
    card.style="width: 100%;";
    var card_img = document.createElement("img");
    card_img.classList.add("card-img-top")
    var card_body = document.createElement("div");
    card_body.classList.add("card-body");
    var btn_id = document.createElement("a");
    btn_id.classList.add("button_id_send");
    btn_id.classList.add("btn");
    btn_id.classList.add("btn-primary");
    btn_id.dataset.rowId = id;
    btn_id.id = id;
    btn_id.innerText = "id: " + id;
    card_body.prepend(btn_id);
    card.prepend(card_body);
    card.prepend(card_img);

    setSrcID(card_img, id);
    if (pr) {
        $("#history-group").prepend(card)
    }else{
        $("#history-group").append(card);
    }

    $(btn_id).on("click", btnClassClick);
 }

var addHistory = function() {
    const xhr_history = new XMLHttpRequest();
    xhr_history.open("GET", "/get_history");
    xhr_history.send();
    xhr_history.onload = function() {
        if (xhr_history.status == 200) {
            var array =  $.parseJSON(xhr_history.response);
            for(var i=0; i < array.length ; i++){
                addHistoryImg(array[i]);
            }
        }
    }
    $(".button_id_send").on("click", btnClassClick);
 }

var btnClassClick = function(e){
    openImage(e.target.dataset.rowId);
}

var setSrcID = function(img_object, id_image){

    const get_img = new XMLHttpRequest();

    get_img.open('GET', '/image/' + id_image);
    get_img.send();
    var rez = "";
    get_img.onload = function() {
        $(img_object).attr("src", "data:image/jpeg;base64,"+$.parseJSON(get_img.response));
    }
}

var openImage = function(id_image){
    setSrcID($(".upload-file"), id_image)
    $("#image-id").attr("data-row-id", id_image)

}

$("#button_upload").click(function(){
    const fileInput = document.getElementById('file-input');

    const file = fileInput.files[0];

    const xhr = new XMLHttpRequest();
    const formData = new FormData();

    formData.append('file', file);

    xhr.open('POST', '/upload_image');
    xhr.send(formData);

    xhr.onload = function() {
        if (xhr.status != 200) {
          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            var response_upload = $.parseJSON(xhr.response);
            openImage(response_upload);
            addHistoryImg(response_upload, pr=true);
        }
    };
});



