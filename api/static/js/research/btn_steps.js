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
    document.getElementById("ul-processing-steps").innerHTML = "";
    const list_rez = Object.keys(proc.rez);
    if (list_rez.includes("words")){
        add_btn_li("Выделить слова", function(){
            drawImage(doc.base_image64);
            drawSegment(proc.rez.words);
        })
        list_rez_words = Object.keys(proc.rez.words[0])
        if (list_rez_words.includes("bold")){
            add_btn_li("Выделить начертание слов", function(){
                drawImage(proc.rez.image64_binary);
                for(var i =0; i< proc.rez.words.length; i++){
                    proc.rez.words[i].label = proc.rez.words[i].bold;
                    if (proc.rez.words[i].bold > 0.6){
                        proc.rez.words[i].color = "rgba(0, 255, 0, 0.5)";
                    }else if (proc.rez.words[i].bold < 0.4){
                        proc.rez.words[i].color = "rgba(0, 0, 255, 0.5)";
                    }else{
                        proc.rez.words[i].color = "rgba(255, 0, 0, 0.5)";
                    }
                }
                drawSegment(proc.rez.words);
            })
        }
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
    if (list_rez.includes("neighbors") && list_rez.includes("words")){
        add_btn_li("Ближайшие соседи", function(){
            drawImage(doc.base_image64);
            drawNeighbordGraphWords(proc.rez.neighbors, proc.rez.words);
        })
    }
}