var view_image = function(){
    readDocumentImage(doc.id);
}

var readDocumentImage = function(id){
    const xml = new XMLHttpRequest();
    xml.open("GET", "/doc/read/"+id);
    xml.send();
    xml.onload = function() {
      if (xml.status == 200) {
        var doc_response =  $.parseJSON(xml.response);
        doc.base_image64 = doc_response.image64;
        doc.name = doc_response.name;
        drawImage(doc.base_image64);
      }
    }
}
view_image();