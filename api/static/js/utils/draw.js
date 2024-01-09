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