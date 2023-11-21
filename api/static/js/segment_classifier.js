const type_segment_classifier = document.getElementById('type-segment-classifier-input');
process.type_segment_classifier = 1;
process.list_type_segment_classifier = [1, 2];

type_segment_classifier.onchange = function(){
    process.segments = new Array();
    process.first_point = {};
    process.type_segment_classifier = type_segment_classifier.value;
    select_type_segment_classifier(process.type_segment_classifier);
}

var function_segment_classifier_1 = function(){
//    const xhr = new XMLHttpRequest();
//    const formData = new FormData();
//    const edges = process.edges;
//    const points = process.points;
//    const mandatory_links = process.bboxes_edge;
//    const threshold = document.getElementById('threshold_segment_input').value;
//    formData.append('edges', JSON.stringify(edges));
//    formData.append('points', JSON.stringify(points));
//    formData.append('threshold', threshold);
//    formData.append('mandatory_links', JSON.stringify(mandatory_links));
//
//    xhr.open('POST', '/width_segments');
//    xhr.send(formData);
//
//    xhr.onload = function() {
//        if (xhr.status != 200) {
//          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
//        } else {
//            var response_segment = $.parseJSON(xhr.response);
//            process.segment = response_segment;
//            process.exist_data_step["segment"] = true;
//            functionSegmentStep();
//        }
//    };
}

var function_segment_classifier_2 = function(){
//    const xhr = new XMLHttpRequest();
//    const formData = new FormData();
//    const edges = process.edges;
//    const points = process.points;
//    const mandatory_links = process.bboxes_edge;
//    const delete_edges = process.delete_edges;
//    console.log("delete edges", delete_edges);
//    formData.append('edges', JSON.stringify(edges));
//    formData.append('points', JSON.stringify(points));
//    formData.append('delete_edges', JSON.stringify(delete_edges));
//    formData.append('mandatory_links', JSON.stringify(mandatory_links));
//
//    xhr.open('POST', '/manual_segments');
//    xhr.send(formData);
//
//    xhr.onload = function() {
//        if (xhr.status != 200) {
//          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
//        } else {
//            console.log("SERVER SEGMENT MANUAL FINISH");
//            var response_segment = $.parseJSON(xhr.response);
//            process.segment = response_segment;
//            process.exist_data_step["segment"] = true;
//            functionSegmentStep();
//        }
//    };
}

process.function_segment_classifier = {
    1: function_segment_classifier_1,
    2: function_segment_classifier_2,
}

var select_type_segment_classifier = function(num_type) {
    $(".segment-classifier-subsegment").css("display", "none");
    $("#type-segment-classifier-"+num_type).css("display" ,"block");
}

var functionStartSegmentClassifierStep = function(){
    console.log("start Segment classifier");
    $("#segment-label-list").css("display" ,"block");
    addLabels();
}

var functionSegmentClassifierStep = function(){
    if (process.exist_data_step["segment-classifier"]){
        functionImageStep();
//        unlockStep("segment");

    }
}

var addSegmentLabel = function(id, text, pr=false) {
    process.labels.push({"id": id, "name": text});
    var radio = document.createElement('input');
    radio.classList.add("form-check-input");
    radio.type = "radio";
    radio.name = "typeLabel";
    radio.id = "typeLabel"+id;
    var text_label = document.createElement('label');
    text_label.classList.add("form-check-label");
    text_label.for = "typeLabel"+id;
    text_label.innerText = text + "(id: " + id + ")";
    var label = document.createElement('li');
    label.classList.add("label");
    label.classList.add("form-check");
    label.dataset.rowId = id;

    label.prepend(radio);
    label.prepend(text_label);

    if (pr) {
        $("#label-group").prepend(label)
    }else{
        $("#label-group").append(label);
    }
 }

 var addLabels = function() {
    const xhr_labels = new XMLHttpRequest();
    xhr_labels.open("GET", "/get_labels");
    xhr_labels.send();
    xhr_labels.onload = function() {
        if (xhr_labels.status == 200) {
            var array =  $.parseJSON(xhr_labels.response);
            $("#label-group")[0].innerText = "";
            process.labels = new Array();
            for(var i=0; i < array.length ; i++){
                addSegmentLabel(array[i].id, array[i].name);
            }
        }
    }
//    $(".button_id_send").on("click", btnClassClick);
}

$("#button_new_label").click(function(){
    const xhr_create_label = new XMLHttpRequest();
    const formData = new FormData();
    const name = document.getElementById('nameNewLabel').value;
    formData.append('name', name);
    xhr_create_label.open("POST", "/create_label");
    xhr_create_label.send(formData);
    xhr_create_label.onload = function() {
        if (xhr_create_label.status == 200) {
            var new_id =  $.parseJSON(xhr_create_label.response);

            addSegmentLabel(new_id, name);

        }
    }
});

var activeLabel = function(){
    var list_label = $("#label-group")[0].children;
    for (var i = 0; i < list_label.length; i++){
        const label = list_label[i];
        if (label.children[1].checked){
            return label.dataset.rowId;
        }
    }
}