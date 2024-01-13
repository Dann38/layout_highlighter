var set_btn = function(btn, text_btn, class_btn, fun){
    btn.className = class_btn;
    btn.innerHTML = text_btn;
    btn.addEventListener("click", fun);
}

var set_mouse_canvas = function(canvas){
  doc.mousedown = {};
  doc.mousemove = {};
  doc.mousedown.fun = function(x, y){};
  doc.mousemove.fun = function(x, y){};
  canvas.addEventListener('mousedown', function (e) {
      const rect = canvas.getBoundingClientRect()
      const c = doc.width_image/canvas.clientWidth;
      var x = c*(e.clientX - rect.left);
      var y = c*(e.clientY - rect.top);
      type_segment_mousedown(x, y);
  });
  canvas.addEventListener('mousemove', function (e) {
      const rect = canvas.getBoundingClientRect()
      const c = doc.width_image/canvas.clientWidth;
      var x = c*(e.clientX - rect.left);
      var y = c*(e.clientY - rect.top);
      type_segment_mousemove(x, y)
  });
}

var type_segment_mousedown = function(x, y){
  doc.mousedown.fun(x, y);
}

var type_segment_mousemove = function(x, y){
  doc.mousemove.fun(x, y);
}

var is_into_rect = function(x, y, rx0, ry0, rx1, ry1) {
  var x0 = Math.min(rx0, rx1);
  var x1 = Math.max(rx0, rx1);
  var y0 = Math.min(ry0, ry1);
  var y1 = Math.max(ry0, ry1);
  return x > x0 && x < x1 && y > y0 && y < y1;
}