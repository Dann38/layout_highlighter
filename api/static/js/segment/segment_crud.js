const menu_segment = document.getElementById('menu-segment');
doc.segment = {}

var add_segment = function(segment){
    var card = $('\
    <div id="card-segment-'+segment.id+'" class="card card-dataset col-sm-2">\
        <div class="card-body">\
        </div>\
        <h5 class="card-title">'+segment.id+'(doc:'+segment.document_id + ' mark: '+segment.marking_id+')</h5>\
    </div>\
    ')

    $("#menu-segment").append(card);
    card.click(function(){openSegment(segment.id)})
}

var openSegment = function(segment_id){
    selectSegment(doc.segment.id, segment_id);
    const xml = new XMLHttpRequest();
    xml.open("GET", "/segmentdata/read/"+segment_id)
    xml.send();
    xml.onload = function() {
        if (xml.status == 200) {
            var rez =  $.parseJSON($.parseJSON(xml.response));
            console.log(rez)
            doc.segment = rez;
            doc.segment.id = segment_id;
            miniDrawImage(rez.image64);
        }
    }

}

var selectSegment = function(old_id, new_id){
    $("#card-segment-"+old_id).removeClass("bg-primary");
    $("#card-segment-"+new_id).addClass("bg-primary");
}

var deleteSegment = function(segment_id){
      const xml = new XMLHttpRequest();
      xml.open('POST', '/segmentdata/delete/'+segment_id);
      xml.send();
      xml.onload = function() {
         miniDrawImage("")
         $("#card-segment-"+segment_id).remove();
      }
}

var view_segment_menu = function(){
    menu_segment.innerText = "";

    const xml = new XMLHttpRequest();
    xml.open("GET", "/dataset/"+open_dataset.id+"/segments/read/");
    xml.send();
    xml.onload = function() {
        if (xml.status == 200) {
            var array =  $.parseJSON(xml.response);
            for(var i=0; i < array.length ; i++){
                add_segment(array[i]);
            }
        }
    }
}

view_segment_menu();

$("#segment-delete").click(function(){
    deleteSegment(doc.segment.id)
})
