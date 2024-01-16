const body_table_marking = $("#table-marking")[0].children[1];
const dataset = {}

var add_marking = function(marking){
    var row = document.createElement("tr");
  
    var name = document.createElement("td");
    name.innerHTML = marking.name;
    var btn = document.createElement("td");
    var delete_btn = document.createElement("button");

    set_btn(delete_btn, "Del", "btn btn-outline-danger", function(){
        deleteMarking(marking.id);
        row.remove();
    })
    btn.append(delete_btn);

    row.append(name);
    row.append(btn);

    row.className = "marking-row";
    row.dataset.id=marking.id
    body_table_marking.append(row);  
}

var view_marking = function(dataset_id){
    dataset.id = dataset_id;
    body_table_marking.innerHTML = ""
    
    const xml = new XMLHttpRequest();
    xml.open("GET", "/dataset/"+dataset_id+"/markingsegment/read/");
    xml.send();
    xml.onload = function() {
        if (xml.status == 200) {
            var array =  $.parseJSON(xml.response);
            
            for(var i=0; i < array.length ; i++){
                add_marking(array[i]);
            }
        }
    }
}

var deleteMarking = function(marking_id){
    const xml = new XMLHttpRequest();
    xml.open("POST", "/markingsegment/delete/"+marking_id);
    xml.send();
    xml.onload = function() {
    }
}

var addMarking = function(){
    const xml = new XMLHttpRequest();
    const formData = new FormData();

    var name = document.getElementById("name-new-marking").value;
    formData.append("name", name);
    formData.append("dataset_id", dataset.id);

    xml.open("POST", "/markingsegment/create/");
    xml.send(formData);
    xml.onload = function() {
        if (xml.status == 200) {
            var marking =  $.parseJSON(xml.response);
            add_marking(marking);
        }
    }

}

$("#btn-add-new-marking").click(function(){
    addMarking()
})