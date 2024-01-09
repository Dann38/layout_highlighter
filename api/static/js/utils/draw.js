const canvas = document.getElementById("image-rez");
const ctx = canvas.getContext("2d");

var drawImage = function (base64) {
    const img = new Image();
    img.src = "data:image/jpeg;base64,"+base64;
  
    var width_image = img.width;
    var height_image = img.height;
    doc.width_image = width_image;
    doc.height_image = height_image;
  
    canvas.width = img.width;
    canvas.height = img.height;
    canvas.style.width = "100%";
  
    ctx.drawImage(img,  0, 0,  img.width, img.height)
    doc.coef_image =  canvas.width/img.width;
}

var drawSegment = function (segments) {
    for(var i = 0; i < segments.length; i++){
        
        drawRectangle(segments[i].x_top_left, 
            segments[i].y_top_left, 
            segments[i].x_bottom_right, 
            segments[i].y_bottom_right); 
    }
}

var drawRectangle = function(x_top_left, y_top_left, x_bottom_right, y_bottom_right) {
    const coef = doc.coef_image

    const x0 = coef*x_top_left;
    const x1 = coef*x_bottom_right;
    const y0 = coef*y_top_left;
    const y1 = coef*y_bottom_right;
    console.log(x0, x1, y0, y1);
    ctx.beginPath();
    ctx.strokeStyle = "rgba(255, 0, 0, 0.5)";
    ctx.lineWidth = 5;
    ctx.moveTo(x0, y0);
    ctx.lineTo(x0, y1);
    ctx.lineTo(x1, y1);
    ctx.lineTo(x1, y0);
    ctx.closePath();
    ctx.stroke();
}
