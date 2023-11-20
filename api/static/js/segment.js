const type_segmentor = document.getElementById('type-segment-input');
process.type_segmentor = 1;
process.list_type_segmentor = [1, 2];

type_segmentor.onchange = function(){
    process.delete_edges = new Array();
    process.first_point = {};
    process.type_segmentor = type_segmentor.value;
    select_type_segmentor(process.type_segmentor);
    writeCurrentLayout();
}

var function_segmentor_1 = function(){
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

    xhr.open('POST', '/width_segments');
    xhr.send(formData);

    xhr.onload = function() {
        if (xhr.status != 200) {
          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            var response_segment = $.parseJSON(xhr.response);
            process.segment = response_segment;
            process.exist_data_step["segment"] = true;
            functionSegmentStep();
        }
    };
}

var function_segmentor_2 = function(){
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    const edges = process.edges;
    const points = process.points;
    const mandatory_links = process.bboxes_edge;
    const delete_edges = process.delete_edges;
    console.log("delete edges", delete_edges);
    formData.append('edges', JSON.stringify(edges));
    formData.append('points', JSON.stringify(points));
    formData.append('delete_edges', JSON.stringify(delete_edges));
    formData.append('mandatory_links', JSON.stringify(mandatory_links));

    xhr.open('POST', '/manual_segments');
    xhr.send(formData);

    xhr.onload = function() {
        if (xhr.status != 200) {
          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            console.log("SERVER SEGMENT MANUAL FINISH");
            var response_segment = $.parseJSON(xhr.response);
            process.segment = response_segment;
            process.exist_data_step["segment"] = true;
            functionSegmentStep();
        }
    };
}

process.function_segmentor = {
    1: function_segmentor_1,
    2: function_segmentor_2,
}

var select_type_segmentor = function(num_type) {
    $(".segment-subsegment").css("display", "none");
    $("#type-segment-"+num_type).css("display" ,"block");
}


const look_graph = document.getElementById('segment_graph');
look_graph.onchange = function(){
    functionSegmentStep();
}

$("#button_segment").click(function(){
    process.function_segmentor[process.type_segmentor]();
});

var functionSegmentStep = function(){
    if (process.exist_data_step["segment"]){
        functionImageStep();
        for(var i = 0; i < process.segment.length; i++){
            const seg = process.segment[i];
            const rect = graphToRectBboxes(seg);
            writeRectangle(rect.x_left, rect.y_top, rect.x_right-rect.x_left, rect.y_bottom-rect.y_top);

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

var plotWidthBar = function(){
    const max_width = 150;
    const step = 5;
    const count_bar = Math.round(max_width/step);
    let arr = new Array(count_bar).fill(0);
    for (var i = 0; i < process.edges.length; i++){
        var ind = Math.round(process.edges[i].width / step);
        if (ind >= count_bar){
            arr[count_bar-1] += 1
        }else {
            arr[ind] += 1;
        }
    }
    let arr_label = new Array(count_bar)
    for (var i=0; i < count_bar; i++){
        arr_label[i] = i*step + step/2;
    }
    const canvas = document.getElementById('width-edge')
    const ctx = canvas.getContext('2d');
    // рисуем фон
    ctx.fillStyle = "white";
    canvas.height = canvas.width
    ctx.fillRect(0,0,canvas.width, canvas.height);

    // рисуем данные
    ctx.fillStyle = "blue";
    let arr_rez = new Array(count_bar).fill(0);
    for (var i = 0; i < count_bar; i++){
        if (isNaN(arr[i])) {
            arr_rez[i] = 0;
        }else{
            arr_rez[i] = arr[i];
        }

    }
    arr = arr_rez;
    const canvas_step = canvas.width/(count_bar+4)
    const h_step = canvas.height/ Math.round(Math.max(... arr)+2)
    for(var i=0; i<count_bar; i++) {
      var dp = arr[i]*h_step;
      ctx.fillRect(2*canvas_step + i*canvas_step, canvas.height-dp , canvas_step, dp);
    }
//    for(var i=0; i<count_bar; i++) {
//      ctx.fillText(arr_label[i], canvas_step + i*canvas_step, canvas.height);
//    }
}

var graphToRectBboxes = function(seg){
    const c = process.points.length / process.bboxes.length; // ОШИБКА ТОЧЕК МОЖЕТ БЫТЬ В СПОСОБЕ ОПРЕДЕЛЕНИЯ КАКОМУ BBOX ПРИНАДЛЕЖИТ ТОЧКА;
    const bbox = process.bboxes[Math.floor(seg.list_index_point[0]/c)];
    const rect = {
        "x_left": bbox.x_top_left,
        "y_top": bbox.y_top_left,
        "x_right": bbox.x_top_left + bbox.width,
        "y_bottom": bbox.y_top_left + bbox.height,
    };
    for(var j = 1; j < seg.list_index_point.length; j++){

        const bbox = process.bboxes[Math.floor(seg.list_index_point[j]/c)];
        const x_left =  bbox.x_top_left;
        const y_top = bbox.y_top_left;
        const x_right = bbox.x_top_left + bbox.width;
        const y_bottom = bbox.y_top_left + bbox.height;
        if (rect.x_left > x_left){
            rect.x_left = x_left;
        }
        if (rect.y_top > y_top){
            rect.y_top = y_top;
        }
        if (rect.x_right < x_right){
            rect.x_right = x_right;
        }
        if (rect.y_bottom < y_bottom){
            rect.y_bottom = y_bottom;
        }
    }
    return rect;
}