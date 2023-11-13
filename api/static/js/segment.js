$("#button_segment").click(function(){

    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    const bboxes = process.bboxes;
    const points = process.points;
    const threshold = document.getElementById('threshold-segment-input').value
    formData.append('bboxes', JSON.stringify(bboxes));
    formData.append('points', JSON.stringify(points));
    formData.append('threshold', JSON.stringify(threshold));

    xhr.open('POST', '/delone_to_segment');
    xhr.send(formData);

    xhr.onload = function() {
        if (xhr.status != 200) {
          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            var response_segment = $.parseJSON(xhr.response);
            console.log(response_segment);
            process.exist_data_step["segment"] = true;
            functionSegmentStep();
        }
    };
});
var functionSegmentStep = function(){
    if (process.exist_data_step["segment"]){
        console.log("write segment");
    }
//
//    unlockStep("graph");
}