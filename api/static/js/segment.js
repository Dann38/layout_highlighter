const look_graph = document.getElementById('segment_graph');
look_graph.onchange = function(){
    functionSegmentStep();
}
$("#button_segment").click(function(){

    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    const edges = process.edges;
    const points = process.points;
    const mandatory_links = process.bboxes_edge;
    const threshold = document.getElementById('threshold_segment_input').value;
    formData.append('edges', JSON.stringify(edges));
    formData.append('points', JSON.stringify(points));
    formData.append('threshold', threshold);
    formData.append('mandatory_links', JSON.stringify(mandatory_links));

    xhr.open('POST', '/delone_to_segment');
    xhr.send(formData);

    xhr.onload = function() {
        if (xhr.status != 200) {
          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            var response_segment = $.parseJSON(xhr.response);
            console.log(response_segment);
            process.segment = response_segment;
            process.exist_data_step["segment"] = true;
            functionSegmentStep();
        }
    };
});
var functionSegmentStep = function(){
    if (process.exist_data_step["segment"]){
        functionImageStep();
        for(var i = 0; i < process.segment.length; i++){
            const seg = process.segment[i];
            console.log(seg.x_left, seg.y_top, seg.x_right, seg.y_bottom)
            writeRectangle(seg.x_left, seg.y_top, seg.x_right-seg.x_left, seg.y_bottom-seg.y_top);

            if (look_graph.checked){
                for(var j = 0; j < seg.list_index_point.length; j++){
                    const point = process.points[seg.list_index_point[j]];
                    writePoint(point.x, point.y);
                }
                for(var j = 0; j < seg.list_edge.length; j++){
                    const point1 = process.points[seg.list_edge[j].node1];
                    const point2 = process.points[seg.list_edge[j].node2];
                    writeLine(point1.x, point1.y, point2.x, point2.y, "rgba(0, 0, 255, 0.5)");
                }
            }
        }
    }
//
//    unlockStep("graph");
}

