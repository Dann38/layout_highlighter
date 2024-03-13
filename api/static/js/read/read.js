var addDocument = function() {
    const xml = new XMLHttpRequest();
    const formData = new FormData();
    
  
    const fileInput = document.getElementById('doc-upload-file');
  
    var reader = new FileReader();
    
    reader.onload = function () {
        doc.base_image64 = reader.result.replace("data:", "")
            .replace(/^.+,/, "");
        drawImage(doc.base_image64);
    }
    reader.readAsDataURL(fileInput.files[0]);
}

reading = {
    "select": {},
    "is_select_p1": true,
};
set_mouse_canvas(canvas);

var getInfoBlock = function(){
    const xml = new XMLHttpRequest();
    const formData = new FormData();
    formData.append("base_image64", doc.base_image64);
    var x1_ = Math.round(reading.select.p1.x);
    var x2_ = Math.round(reading.select.p2.x);
    var y1_ = Math.round(reading.select.p1.y);
    var y2_ = Math.round(reading.select.p2.y);
    x1 = Math.min(x1_, x2_)
    x2 = Math.max(x1_, x2_)
    y1 = Math.min(y1_, y2_)
    y2 = Math.max(y1_, y2_)
    formData.append("block", '{"x_top_left":' + x1 + ', "y_top_left":' + y1 + ', "x_bottom_right":' + x2 +', "y_bottom_right":'+ y2 +'}');
    xml.open("POST", "/read/block_info/");
    xml.send(formData);
    xml.onload = function() {
      if (xml.status == 200) {
        var rez =  $.parseJSON($.parseJSON(xml.response));
        document.getElementById("block-label").innerHTML =  rez.label;
        document.getElementById("block-text").innerHTML =  rez.text;
      }
    }
}


var selectBlock = function(){
    drawImage(doc.base_image64);
    
    doc.mousedown.fun = function(x, y){
      if (reading.is_select_p1){
        reading.select = {};
        reading.select.p1 = {"x": x, "y": y};
        reading.is_select_p1 = false;
      }else{
        reading.select.p2 = {"x": x, "y": y};
        console.log(reading.select)
        getInfoBlock();
        reading.is_select_p1 = true
      }
    };
    doc.mousemove.fun = function(x, y){
      drawImage(doc.base_image64);
      if (reading.select.p2 == undefined){
        drawRectangle(reading.select.p1.x, reading.select.p1.y, x, y, "rgba(0, 255, 0, 0.3)");
      }   
      if (reading.select.p2 != undefined){
        drawRectangle(reading.select.p1.x, reading.select.p1.y, reading.select.p2.x, reading.select.p2.y, "rgba(0, 255, 0, 1.0)");  
      }
      
    };
  }



$("#doc-upload-button").click(function(){
    addDocument();
    selectBlock();
})