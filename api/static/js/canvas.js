var addDeleteElement = function(elem, list_elem, delete_=true, add_=true) {
     if (list_elem.includes(elem)) {
        var index = list_elem.indexOf(elem);
        if (index !== -1) {
            if (delete_){
                list_elem.splice(index, 1);
            }

        }
    }else {
        if (add_){
            list_elem.push(elem);
        }
    }
}

var get_edges_point = function(index_point) {
    var list_index_line = new Array();
    for(var i = 0; i < process.edges.length; i++){
        const edge = process.edges[i];

        if (edge.node1 == index_point || edge.node2 == index_point){
            list_index_line.push(i);
        }
    }
    return list_index_line;
}

var get_nearby_point = function(x, y) {
    const zpoint = process.points[0]
    var min = (zpoint.x- x)**2 + (zpoint.y - y)**2;
    var min_index = 0;
    for(var i = 0; i < process.points.length; i++){
        const point = process.points[i];
        const len = (point.x - x)**2 + (point.y - y)**2;
        if (len < min) {
            min = len;
            min_index = i;
        }

    }
    return min_index;
}

var is_into_rect = function(x, y, rx0, ry0, rx1, ry1) {
    var x0 = Math.min(rx0, rx1);
    var x1 = Math.max(rx0, rx1);
    var y0 = Math.min(ry0, ry1);
    var y1 = Math.max(ry0, ry1);
    return x > x0 && x < x1 && y > y0 && y < y1;
}

var get_points_into_rect = function(x0, y0, x1, y1) {
    var array_point = new Array();
    for(var i = 0; i < process.points.length; i++){
        const point = process.points[i];
        if (is_into_rect(point.x, point.y, x0, y0, x1, y1)){
            array_point.push(i);
        }
    }
    return array_point;
}

var get_nearby_center_line = function(x, y) {
    var edges = process.edges

    const edge = edges[0];

    const point1 = process.points[edge.node1];
    const point2 = process.points[edge.node2];

    xc = (point1.x + point2.x)/2;
    yc = (point1.y + point2.y)/2;

    var min = (xc- x)**2 + (yc - y)**2;
    var min_index = 0;
    for(var i = 1; i < edges.length; i++){
        const edge = edges[i];

        const point1 = process.points[edge.node1];
        const point2 = process.points[edge.node2];

        xc = (point1.x + point2.x)/2;
        yc = (point1.y + point2.y)/2;

        var len = (xc- x)**2 + (yc - y)**2;
        if (len < min) {
            min = len;
            min_index = i;
        }

    }
    return min_index;
}

var type_segment_method_edge = function(x, y) {
    index_line = get_nearby_center_line(x, y);
    addDeleteElement(index_line, process.delete_edges);

    for(var i=0; i <  process.delete_edges.length; i++){
        const edge = process.edges[process.delete_edges[i]];
        var point1 = process.points[edge.node1];
        var point2 = process.points[edge.node2];
        writeLine(point1.x, point1.y, point2.x, point2.y, "#ff0000");
    }
}

var type_segment_method_rect = function(x, y) {
    if (process.first_point.x  === undefined){
        process.first_point.x = x;
        process.first_point.y = y;
        console.log(process.first_point);
    }else {
        const x0 = x;
        const y0 = y;
        const x1 = process.first_point.x;
        const y1 = process.first_point.y
        array_point = get_points_into_rect(x0, y0, x1, y1);

        for(var i =0; i < process.edges.length; i++){
            const edge = process.edges[i];
            if (array_point.indexOf(edge.node1) != -1){
                const point = process.points[edge.node2];
                if (!is_into_rect(point.x, point.y, x0, y0, x1, y1)){
                    addDeleteElement(i, process.delete_edges, delete_=false);
                }
            }else if (array_point.indexOf(edge.node2) != -1){
                const point = process.points[edge.node1];
                if (!is_into_rect(point.x, point.y, x0, y0, x1, y1)){
                    addDeleteElement(i, process.delete_edges, delete_=false);
                }
            }
        }
        for(var i=0; i <  process.delete_edges.length; i++){
            const edge = process.edges[process.delete_edges[i]];
            var point1 = process.points[edge.node1];
            var point2 = process.points[edge.node2];
            writeLine(point1.x, point1.y, point2.x, point2.y, "#ff0000");
        }
        process.first_point = {};
    }
}

var setClickCanvas = function(canvas){
    canvas.addEventListener('mousedown', function (e) {
        const canvas_now = document.getElementById("result-image");
        const rect = canvas_now.getBoundingClientRect()
        const c = process.width_image/canvas_now.clientWidth;
        var x = c*(e.clientX - rect.left);
        var y = c*(e.clientY - rect.top);

        if (process.type_segmentor == 2){
            if (typeSegment2method1.checked == true) {
                type_segment_method_edge(x, y);
            }else if (typeSegment2method2.checked == true){
                type_segment_method_rect(x, y);
            }

        }
    });
}

var writeImage = function (base64) {
  const canvas = document.getElementById("result-image");
  const ctx = canvas.getContext("2d");
  const img = new Image();
  img.src = "data:image/jpeg;base64,"+base64;

  var width_image = img.width;
  var height_image = img.height;
  process.width_image = width_image;
  process.height_image = height_image;

  canvas.width = img.width;
  canvas.height = img.height;
  canvas.style.width = "100%";

  ctx.drawImage(img,  0, 0,  img.width, img.height)
  process.coef_image =  canvas.width/img.width;
}

var writeRectangle = function(x_top_left, y_top_left, width, height) {
    const canvas = document.getElementById("result-image");
    const ctx = canvas.getContext("2d");
    const coef = process.coef_image;

    const x0 = x_top_left*coef;
    const x1 = x0 + coef*width;
    const y0 = y_top_left*coef;
    const y1 = y0 + coef*height;

    ctx.beginPath();
    ctx.strokeStyle = "rgba(255, 0, 0, 0.5)";
    ctx.moveTo(x0, y0);
    ctx.lineTo(x0, y1);
    ctx.lineTo(x1, y1);
    ctx.lineTo(x1, y0);
    ctx.closePath();
    ctx.stroke();
}

var writePoint = function(x, y) {
    const canvas = document.getElementById("result-image");
    const ctx = canvas.getContext("2d");
    const coef = process.coef_image;

    const x0 = x*coef;
    const y0 = y*coef;

    size = 2;

    var pointX = Math.round(x0);
    var pointY = Math.round(y0);
    ctx.beginPath();
    ctx.fillStyle = '#00ff00';
    ctx.arc(pointX, pointY, size, 0 * Math.PI, 2 * Math.PI);
    ctx.fill();
}

var writePointRed = function(x, y) {
    const canvas = document.getElementById("result-image");
    const ctx = canvas.getContext("2d");

    const x0 = x;
    const y0 = y;

    size = 4;

    var pointX = Math.round(x0);
    var pointY = Math.round(y0);
    ctx.beginPath();
    ctx.fillStyle = '#ff0000';
    ctx.arc(pointX, pointY, size, 0 * Math.PI, 2 * Math.PI);
    ctx.fill();
}

var writeLine = function(x0, y0, x1, y1, color) {
    const canvas = document.getElementById("result-image");
    const ctx = canvas.getContext("2d");
    const coef = process.coef_image;

    ctx.strokeStyle = color;
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.moveTo(coef*x0, coef*y0);
    ctx.lineTo(coef*x1, coef*y1);
    ctx.stroke();
}

var getLine = function(x0, y0){
    console.log(process.points);
}


const canvas = document.getElementById("result-image");
setClickCanvas(canvas)