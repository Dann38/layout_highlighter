var getDistributionVec = function(){
    const xml = new XMLHttpRequest();
    xml.open("GET", "/segment2vec/distribution/"+doc.segment.id);
    xml.send();
    
    xml.onload = function() {
        if (xml.status == 200) {
            var rez =  $.parseJSON($.parseJSON(xml.response));
            console.log(rez);
        }
    }
}

var getVec = function(){
    const type_vec = $("#segment-select-type-vec").val();
    if (type_vec == 1){ //Распределение
        getDistributionVec();
    }
}

$("#segment-get-vec").click(function(){
    getVec();
})