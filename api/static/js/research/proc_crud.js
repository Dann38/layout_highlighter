var add_row_proc = function(proc){
    const ul = document.getElementById('ul-proc');
    var li = document.createElement("li");
    li.className = "list-group-item";
    var a = document.createElement("a")
    a.setAttribute("href", "#");
    a.innerHTML = proc.name + " ";   
    
    var btn = $('<button type="button" class="btn btn-outline-danger">Del</button>');

    a.addEventListener("click", function(){
        document.getElementById("form-proc-set").value = proc.json_processing;   
    });
    btn[0].addEventListener("click", function(){
        deleteProc(proc.id);
        li.remove();
    });
    li.append(a);
    $(li).append(btn);
    
    

    console.log("add_row_proc");
    document.getElementById('ul-proc').append(li);    
}

var view_proc = function() {
    const ul = document.getElementById('ul-proc');
    ul.innerText = "";
    console.log("VIEW PROC")
    const xml= new XMLHttpRequest();
    xml.open("GET", "/proc/read/");
    xml.send();
    xml.onload = function() {
        if (xml.status == 200) {
            var array =  $.parseJSON(xml.response);
            for(var i=0; i < array.length ; i++){
                add_row_proc(array[i]);
            }
        }
    }
}

var addProc = function() {
    const xml = new XMLHttpRequest();
    const formData = new FormData();
    
  
    const json_processing = document.getElementById("form-proc-set").value;
    const name = document.getElementById('proc-create-name').value;
  
    formData.append('json_processing', json_processing);
    formData.append('name', name);
    console.log(json_processing)
    xml.open('POST', '/proc/create/');
    xml.send(formData);
    xml.onload = function() {
        rez = $.parseJSON(xml.response);
        add_row_proc(rez);

    }
}

var deleteProc = function(id) {
    const xml = new XMLHttpRequest();
    xml.open('GET', '/proc/delete/'+id);
    xml.send();
    xml.onload = function() {
        
    }
  }

view_proc();

$("#proc-create-button").click(function(){
    addProc();
})