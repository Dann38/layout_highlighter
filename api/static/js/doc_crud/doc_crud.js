const menu_docs = document.getElementById('menu-docs');
open_folder = {};
open_folder.history = new Array([0]);

var add_doc = function(doc){
  var card = $('\
    <div class="card card-doc col-sm-3">\
      <img class="card-img-top" src="data:image/jpeg;base64,'+doc.image64+'" alt="doc">\
      <div class="card-body">\
        <h5 class="card-title">'+doc.name+'</h5>\
      </div>\
    </div>\
    ')
  $("#menu-docs").append(card);

  var delete_btn = document.createElement("button");
  var open_btn = document.createElement("button");
  var manual_marking_btn = document.createElement("button");
  set_btn(delete_btn, "Удалить", "btn btn-outline-danger", function(){
    deleteDocument(doc.id);
    card.remove();
  })
  set_btn(open_btn, "Исследовать", "btn btn-outline-success", function(){
    openDocument(doc.id);
  })
  set_btn(manual_marking_btn, "Ручная разметка", "btn btn-outline-success", function(){
    openManualMarking(doc.id);
  })

  card.append(delete_btn)
  card.append(open_btn)
  card.append(manual_marking_btn)
}


var add_folder = function(folder){
  var card = $('\
  <div class="card card-doc col-sm-3">\
    <img class="card-img-top" src="'+src_icon_data_set+'" alt="folder">\
    <div class="card-body">\
      <h5 class="card-title">'+folder.name+'</h5>\
    </div>\
  </div>\
  ')
  $("#menu-docs").prepend(card);

  var delete_btn = document.createElement("button");
  var open_btn = document.createElement("button");
  set_btn(delete_btn, "Удалить", "btn btn-outline-danger", function(){
    deleteFolder(folder.id);
    card.remove();
  })
  set_btn(open_btn, "Открыть", "btn btn-outline-success", function(){
    view_menu(folder.id);
  })


  card.append(delete_btn);
  card.append(open_btn);
}


var view_menu = function(folder_id) {
  var index = open_folder.history.length - 1;
  var id_parent = open_folder.history[index];
  if (id_parent == folder_id){
    open_folder.history.pop();
  }else{
    open_folder.history.push(open_folder.id);
  
  }
  open_folder.id = folder_id;
  menu_docs.innerText = "";
  const xml = new XMLHttpRequest();
  xml.open("GET", "/folder/"+folder_id+"/contents/");
  xml.send();
  xml.onload = function() {
      if (xml.status == 200) {
          var rez =  $.parseJSON(xml.response);
          open_folder.docs_id = rez.documents_id;
          open_folder.folders_id = rez.folders_id;

          for(var i = 0; i < open_folder.docs_id.length; i++){
              view_doc_id(open_folder.docs_id[i]);
          }
          for(var i = 0; i < open_folder.folders_id.length; i++){
              view_folder_id(open_folder.folders_id[i]);
          }
          
      }
  }
}

var view_doc_id = function(doc_id) {
  const xml = new XMLHttpRequest();
  xml.open("GET", "/doc/read/"+doc_id);
  xml.send();
  xml.onload = function() {
      if (xml.status == 200) {
          var doc =  $.parseJSON(xml.response);
          add_doc(doc);
          
      }
  }
}


var view_folder_id = function(folder_id) {
  const xml = new XMLHttpRequest();
  xml.open("GET", "/folder/"+folder_id+"/contents/");
  xml.send();
  xml.onload = function() {
      if (xml.status == 200) {
          var folder =  $.parseJSON(xml.response);
          add_folder(folder);
          console.log()
      }
  }
}

var addDocument = function() {
  const xml = new XMLHttpRequest();
  const formData = new FormData();
  

  const fileInput = document.getElementById('doc-create-file');
  const nameInput = document.getElementById('doc-create-name');

  var reader = new FileReader();
  
  reader.onload = function () {
      base64String = reader.result.replace("data:", "")
          .replace(/^.+,/, "");

      const name = nameInput.value;
    
      formData.append('file', base64String);
      formData.append('name', name);
      formData.append('folder_parent_id', open_folder.id)
    
      xml.open('POST', '/doc/create/');
      xml.send(formData);
      console.log("next");
      xml.onload = function() {
        rez = $.parseJSON(xml.response);
        add_doc(rez);

      }

  }
  reader.readAsDataURL(fileInput.files[0]);
}

var addFolder = function() {
  const xml = new XMLHttpRequest();
  const formData = new FormData();

  const name = document.getElementById('folder-create-name').value;

  formData.append('name', name);
  formData.append('folder_parent_id', open_folder.id)
  xml.open('POST', '/folder/create/');
  xml.send(formData);
  xml.onload = function() {
    folder = $.parseJSON(xml.response);
    add_folder(folder);

  }
}

var deleteDocument = function(id) {
  const xml = new XMLHttpRequest();
  xml.open('GET', '/doc/delete/'+id);
  xml.send();
  xml.onload = function() {

  }
}

var deleteFolder = function(id) {
  const xml = new XMLHttpRequest();
  xml.open('GET', '/folder/delete/'+id);
  xml.send();
  xml.onload = function() {

  }
}

var backFolder =function(){
  var index = open_folder.history.length - 1;
  if (index >= 0){
    var id_parent = open_folder.history[index];
    view_menu(id_parent);
  }
  
}

var openDocument = function(id) {
  window.location.replace("/research/"+id)
}

var openManualMarking = function(id) {
  window.location.replace("/manual_marking/"+id)
}

view_menu(0);

$("#doc-create-button").click(function(){
  addDocument();
})

$("#folder-create-button").click(function(){
  addFolder();
})

$("#back-folder").click(function(){
  backFolder();
})