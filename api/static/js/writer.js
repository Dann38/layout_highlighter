var writeImage = function (base64) {

  const canvas = document.getElementById("result-image");
  const ctx = canvas.getContext("2d");
  const img = new Image();
  img.src = "data:image/jpeg;base64,"+base64;

  var width_image = img.width;
  var height_image = img.height;
  canvas.height = canvas.width * img.height / img.width;

  ctx.drawImage(img,  0, 0,  img.width, img.height,  0, 0,  canvas.width, canvas.height);
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