var add_btn_li = function(text_btn, fun){
    var li = document.createElement("li");
    var a = document.createElement("a");
    a.className = "dropdown-item";
    a.setAttribute("href", "#");
    a.innerHTML = text_btn;
    li.append(a);
    li.addEventListener("click", fun);
    document.getElementById("ul-processing-steps").append(li);
}

var view_btn_steps = function(){
    const list_rez = Object.keys(proc.rez);
    if (list_rez.includes("words")){
        add_btn_li("Выделить слова", function(){
            drawImage(doc.base_image64);
            drawSegment(proc.rez.words);
        })
    }
    if (list_rez.includes("join_blocks")){
        add_btn_li("Выделить блоки", function(){
            drawImage(doc.base_image64);
            drawSegment(proc.rez.join_blocks);
        })
    }
    if (list_rez.includes("no_join_blocks")){
        add_btn_li("Выделить блоки до объединения", function(){
            drawImage(doc.base_image64);
            drawSegment(proc.rez.no_join_blocks);
        })
    }
}