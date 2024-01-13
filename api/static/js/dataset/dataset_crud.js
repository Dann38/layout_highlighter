const menu_dataset = document.getElementById('menu-datasets');

var add_dataset = function(dataset){
    console.log(dataset);
    console.log(src_icon_data_set);
    var card = $('\
    <div class="card card-dataset col-sm-3">\
        <img class="card-img-top" src="'+src_icon_data_set+'" alt="dataset">\
        <div class="card-body">\
        </div>\
        <h5 class="card-title">'+dataset.name+'</h5>\
    </div>\
    ')

    $("#menu-datasets").append(card);

    var delete_btn = document.createElement("button");
    var info_btn = document.createElement("button");
    set_btn(delete_btn, "Удалить", "btn btn-outline-danger", function(){
        deleteDataset(dataset.id);
        card.remove();
    })
    set_btn(info_btn, "Метки", "btn btn-outline-secondary", function(){
        openSetDataset(dataset);
    })
    
    card.append(info_btn);
    card.append(delete_btn);
    
}

var view_dataset_menu = function(){
    menu_dataset.innerText = "";

    const xhr_docs = new XMLHttpRequest();
    xhr_docs.open("GET", "/dataset/read/");
    xhr_docs.send();
    xhr_docs.onload = function() {
        if (xhr_docs.status == 200) {
            var array =  $.parseJSON(xhr_docs.response);
            for(var i=0; i < array.length ; i++){
                add_dataset(array[i]);
            }
        }
    }
}


var deleteDataset = function(dataset_id){
    const xml = new XMLHttpRequest();
    xml.open("POST", "/dataset/delete/"+dataset_id);
    xml.send();
    xml.onload = function() {
    }
}

var openSetDataset = function(dataset){
    $("#dataset-info-name")[0].innerText = dataset.name;
    $("#dataset-info-discription")[0].innerText = dataset.discription;
    view_marking(dataset.id);
    
}

var addDataset = function(){
    const xml = new XMLHttpRequest();
    const formData = new FormData();


    const discription = document.getElementById('dataset-create-discription').value;
    const name = document.getElementById('dataset-create-name').value;

    formData.append('discription', discription);
    formData.append('name', name);

    xml.open('POST', '/dataset/create/');
    xml.send(formData);

    xml.onload = function() {
        rez = $.parseJSON(xml.response);
        add_dataset(rez);
    }
}

view_dataset_menu()

$("#dataset-create-button").click(function(){
    addDataset();
})