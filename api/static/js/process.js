var process = {};
// Для ручной разметки

var openProcessing = function(){
    $("#button_open_processing").text("Новое исследование");
    $("#progress").css("display" ,"block");
    select("image");
}

var addProcess = function(proc){
    const body = $("#body-table-processing")[0];
    var row = document.createElement('tr');

    var col_id = document.createElement("td");
    col_id.innerText = proc.id;
    var col_id_image = document.createElement("div");
    col_id_image.innerText = proc.id_image;

    row.append(col_id);
    row.append(col_id_image);
    body.prepend(row);

    row.onclick = function(){
        console.log("click", proc);
        clickProcess(proc);
    };
}

var addProcesses = function(){
    const xhr_process = new XMLHttpRequest();
    xhr_process.open("GET", "/get_processes");
    xhr_process.send();
    xhr_process.onload = function() {
        if (xhr_process.status == 200) {
            var array =  $.parseJSON(xhr_process.response);
            for(var i=0; i < array.length ; i++){
                addProcess(array[i]);
            }
        }
    }
}

var clickProcess = function(proc){
    openProcessing();
    openImage(proc.id_image);
    process.id = proc.id;

    unlockStep("tesseract");
    select("tesseract");
//
//    unlockStep("graph");
//    select("graph");

}

addProcesses();