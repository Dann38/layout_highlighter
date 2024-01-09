var add_row_doc = function(doc){

  const table = document.getElementById('table-docs');
  const body_table = table.children[1];

  var row = document.createElement("tr");

  var name = document.createElement("td");
  var image = document.createElement("td");
  image.className = "w-60";

  name.innerText = doc.name
  var image64 =  document.createElement("img");

  image64.setAttribute("src", "data:image/jpeg;base64,"+doc.image64)
  image64.className = "d-block w-100";
  image.append(image64);


  row.append(name);
  row.append(image);

  row.className = "doc-row";
  row.dataset.id=doc.id
  body_table.append(row);
}

var view_table = function() {
  const table = document.getElementById('table-docs');
  const body_table = table.children[1];
  body_table.innerText = "";

  const xhr_docs = new XMLHttpRequest();
  xhr_docs.open("GET", "/doc/read/");
  xhr_docs.send();
  xhr_docs.onload = function() {
      if (xhr_docs.status == 200) {
          var array =  $.parseJSON(xhr_docs.response);
          for(var i=0; i < array.length ; i++){
              add_row_doc(array[i]);
          }
          rows = $(".doc-row");
          for(var i=0; i < array.length; i++){

              // rows[i].onclick = function(e){
              //     open_cow.status= "old"
              //     open_cow.id = this.dataset.id
              //     open_cow_menu();
              // };
          }
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
        add_row_doc(rez);
        
      }

  }
  reader.readAsDataURL(fileInput.files[0]);
}

view_table();

$("#doc-create-button").click(function(){
  addDocument();
})