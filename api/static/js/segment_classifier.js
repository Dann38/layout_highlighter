const type_segment_classifier = document.getElementById('type-segment-classifier-input');
process.type_segment_classifier = 1;
process.type_segment_classifier = [1, 2];

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


var functionSegmentClassifierStep = function(){
    if (process.exist_data_step["segment-classifier"]){
        functionImageStep();
//        unlockStep("segment");

    }
}