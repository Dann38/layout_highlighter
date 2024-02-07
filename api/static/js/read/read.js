var addDocument = function() {
    const xml = new XMLHttpRequest();
    const formData = new FormData();
    
  
    const fileInput = document.getElementById('doc-upload-file');
  
    var reader = new FileReader();
    
    reader.onload = function () {
        base64String = reader.result.replace("data:", "")
            .replace(/^.+,/, "");
      
        formData.append('file', base64String);
      
        xml.open('POST', '/read/upload/');
        xml.send(formData);
        console.log("next");
        xml.onload = function() {
          rez = $.parseJSON(xml.response);
          add_doc(rez);
        }
  
    }
    reader.readAsDataURL(fileInput.files[0]);
}
