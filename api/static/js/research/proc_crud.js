var add_row_proc = function(proc){
  const table = document.getElementById('table-proc');
  const body_table = table.children[1];

  var row = document.createElement("tr");
  
  var name = document.createElement("td");
  var name_btn = document.createElement("button");
  var btn = document.createElement("td");
  var delete_btn = document.createElement("button");
  
  
  set_btn(name_btn, proc.name, "btn btn-outline-primary", function(){
    openProc(proc)
  })
  set_btn(delete_btn, "Del", "btn btn-danger", function(){
    deleteProc(proc.id);
    row.remove();
  })
  btn.append(delete_btn);
  name.append(name_btn)

  row.append(name);
  row.append(btn);

  row.className = "proc-row";
  row.dataset.id=proc.id
  body_table.append(row);   
}

var view_proc = function() {
    const table = document.getElementById('table-proc');
    const body_table = table.children[1];
    body_table.innerText = "";
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


var openProc = function(proc) {
    document.getElementById("form-proc-set").value = proc.json_processing;
    document.getElementById("name-proc").innerHTML = proc.name;
}
view_proc();

$("#proc-create-button").click(function(){
    addProc();
})