$("#button_graph").click(function(){

    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    const bboxes = process.bboxes;
    const count = document.getElementById('count-point-input').value;
    formData.append('bboxes', JSON.stringify(bboxes));
    formData.append('count', count);
    xhr.open('POST', '/graph_process');
    xhr.send(formData);

    xhr.onload = function() {
        if (xhr.status != 200) {
          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            var response_bboxes = $.parseJSON(xhr.response);
            const points = response_bboxes.list_point;
            const edges = response_bboxes.list_edge;
            const bboxes_edge = response_bboxes.bboxes_edge
            process.points = points;
            process.edges = edges;
            process.bboxes_edge = bboxes_edge;
            process.exist_data_step["graph"] = true;
            functionGraphStep();
        }
    };
});

var functionStartGraphStep = function() {}

var functionGraphStep = function(){
    if (process.exist_data_step["graph"]){
        functionImageStep();
        for(var i = 0; i < process.points.length; i++){
            const point = process.points[i];
            writePoint(point.x, point.y);
        }
        for(var i = 0; i < process.edges.length; i++){
            const point1 = process.points[process.edges[i].node1];
            const point2 = process.points[process.edges[i].node2];
            writeLine(point1.x, point1.y, point2.x, point2.y, "rgba(0, 0, 255, 0.5)");
        }
        unlockStep("segment");
        plotWidthBar();
    }
}
