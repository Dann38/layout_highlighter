var set_btn = function(btn, text_btn, class_btn, fun){
    btn.className = class_btn;
    btn.innerHTML = text_btn;
    btn.addEventListener("click", fun);
  }
  