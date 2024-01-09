var processingImage = function(){
    const xml = new XMLHttpRequest();
    const formData = new FormData();
    const json_set = document.getElementById("form-proc-set").value
    formData.append("doc_id", doc.id);
    formData.append("proc_set", json_set);
    xml.open("POST", "/doc/research/");
    xml.send(formData);

    xml.onload = function() {
      if (xml.status == 200) {
        var rez =  $.parseJSON($.parseJSON(xml.response));
        proc.rez = rez;
        view_btn_steps();
      }
    }
}

$("#btn-processing").click(function(){
    processingImage();
})