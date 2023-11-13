var writeImage = function (base64) {

  const canvas = document.getElementById("result-image");
  const ctx = canvas.getContext("2d");
  const img = new Image();
  img.src = "data:image/jpeg;base64,"+base64;
  console.log(img);
  var width_image = img.width;
  var height_image = img.height;
  canvas.height = canvas.width * img.height / img.width;

  ctx.drawImage(img,  0, 0,  img.width, img.height,  0, 0,  canvas.width, canvas.height);
  $("#result-image").attr("data-coef", canvas.width/img.width);
}

var writeRectangle = function(x_top_left, y_top_left, width, height) {
    const canvas = document.getElementById("result-image");
    const ctx = canvas.getContext("2d");
    const coef = $("#result-image")[0].dataset["coef"];

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