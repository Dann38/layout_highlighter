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

var view_menu = function() {
  const menu_docs = document.getElementById('menu-docs');
  menu_docs.innerText = "";

  const xhr_docs = new XMLHttpRequest();
  xhr_docs.open("GET", "/doc/read/");
  xhr_docs.send();
  xhr_docs.onload = function() {
      if (xhr_docs.status == 200) {
          var array =  $.parseJSON(xhr_docs.response);
          for(var i=0; i < array.length ; i++){
              add_doc(array[i]);
          }
          rows = $(".doc-row");
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

var deleteDocument = function(id) {
  const xml = new XMLHttpRequest();
  xml.open('GET', '/doc/delete/'+id);
  xml.send();
  xml.onload = function() {

  }
}

var openDocument = function(id) {
  window.location.replace("/research/"+id)
}

var openManualMarking = function(id) {
  window.location.replace("/manual_marking/"+id)
}

view_menu();

$("#doc-create-button").click(function(){
  addDocument();
})