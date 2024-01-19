var getDistributionVec = function(){
    const xml = new XMLHttpRequest();
    xml.open("GET", "/segment2vec/distribution/"+doc.segment.id);
    xml.send();
    
    xml.onload = function() {
        if (xml.status == 200) {
            var rez =  $.parseJSON($.parseJSON(xml.response));
            $("#segment-info-vec").val(rez.vec);
        }
    }
}

var getVec = function(){
    const type_vec = $("#segment-select-type-vec").val();
    if (type_vec == 1){ //Распределение
        getDistributionVec();
    }
}

var createJsonDataset = function(){
    const parm = $("#np-dataset-create-setting").val();
    
    const xml = new XMLHttpRequest();
    const formData = new FormData();

    xml.open("POST", "/files/np_dataset/"+open_dataset.id);
    
    formData.append('parm', parm);
    xml.send(formData);
    
    xml.onload = function() {
        if (xml.status == 200) {
            download($.parseJSON(xml.response), "data.json");
        }
    }
}

$("#segment-get-vec").click(function(){
    getVec();
})


$("#np-dataset-create-button").click(function(){
    createJsonDataset();
})