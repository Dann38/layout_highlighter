const tools = {};
tools.font_size = 20;

var autoBlock = function(){
    const xml = new XMLHttpRequest();
    const formData = new FormData();
    formData.append("doc_id", doc.id);
    formData.append("proc_set", '{"save_blocks":true}');
    
    xml.open("POST", "/doc/research/");
    xml.send(formData);

    xml.onload = function() {
      if (xml.status == 200) {
        var rez =  $.parseJSON($.parseJSON(xml.response));
        marking.blocks = rez.join_blocks;
        drawImage(doc.base_image64);
        drawSegment(marking.blocks);
      }
    }
}
var action_block = function(x, y){
  for(var i = 0; i < marking.blocks.length; i++){
    const block = marking.blocks[i]
    var is_into_block = is_into_rect(x, y, block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right);
    if (is_into_block) {
      marking.action_block = i; 
    }
  }

}
var horizontalScissors = function(){
  drawImage(doc.base_image64);
  drawSegment(marking.blocks);
  doc.mousedown.fun = function(x, y){
    console.log("action_block: ");
    console.log(marking.blocks[marking.action_block]);
    // marking.blocks.splice(marking.action_block, 1);
    var b1 = marking.blocks[marking.action_block];
    var b2 = {}
    b2.x_top_left = b1.x_top_left;
    b2.y_top_left = y+1;
    b2.x_bottom_right = b1.x_bottom_right;
    b2.y_bottom_right = b1.y_bottom_right;
    b1.y_bottom_right = y-1;
    marking.blocks.push(b2);
  };
  doc.mousemove.fun = function(x, y){
    drawImage(doc.base_image64);
    action_block(x, y);
    for(var i = 0; i < marking.blocks.length; i++){
      const block = marking.blocks[i];
      if (i == marking.action_block){
          drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(0, 255, 0, 0.5)");
          drawLine(block.x_top_left,y, block.x_bottom_right, y, "rgba(0, 255, 0, 0.5)");
      }else{
          drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(255, 0, 0, 0.5)");
      }
      
    }
    
  };
}

var verticalScissors = function(){
  drawImage(doc.base_image64);
  drawSegment(marking.blocks);
  doc.mousedown.fun = function(x, y){
    console.log("action_block: ");
    console.log(marking.blocks[marking.action_block]);
    // marking.blocks.splice(marking.action_block, 1);
    var b1 = marking.blocks[marking.action_block];
    var b2 = {};
    b2.y_top_left = b1.y_top_left;
    b2.x_top_left = x+1;
    b2.y_bottom_right = b1.y_bottom_right;
    b2.x_bottom_right = b1.x_bottom_right;
    b1.x_bottom_right = x-1;
    marking.blocks.push(b2);
  };
  doc.mousemove.fun = function(x, y){
    drawImage(doc.base_image64);
    action_block(x, y);
    for(var i = 0; i < marking.blocks.length; i++){
      const block = marking.blocks[i];
      if (i == marking.action_block){
          drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(0, 255, 0, 0.5)");
          drawLine(x, block.y_top_left, x, block.y_bottom_right, "rgba(0, 255, 0, 0.5)");
      }else{
          drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(255, 0, 0, 0.5)");
      }
      
    }
    
  };
}
var deleteBlock = function(){
  drawImage(doc.base_image64);
  drawSegment(marking.blocks);
  doc.mousedown.fun = function(x, y){
    console.log("action_block: ");
    console.log(marking.blocks[marking.action_block]);
    marking.blocks.splice(marking.action_block, 1);
  };
  doc.mousemove.fun = function(x, y){
    drawImage(doc.base_image64);
    action_block(x, y);
    for(var i = 0; i < marking.blocks.length; i++){
      const block = marking.blocks[i];
      if (i == marking.action_block){
          drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(255, 0, 0, 0.5)");
      }else{
          drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(0, 255, 0, 0.5)");
      }
      
    }
    
  };
}

var joinBlock = function(){
  var is_first_click = true; 
  var first_action_block = undefined;
  drawImage(doc.base_image64);
  drawSegment(marking.blocks);
  
  doc.mousedown.fun = function(x, y){
    if (is_first_click){
      first_action_block = marking.action_block;
      is_first_click = false;
    }else if(first_action_block == marking.action_block){
      first_action_block = undefined;
      is_first_click = true;
    }else{
      console.log("action_block: ");

      var b1 = marking.blocks[first_action_block]
      var b2 = marking.blocks[marking.action_block]
      b1.x_top_left = Math.min(b1.x_top_left, b2.x_top_left)
      b1.y_top_left = Math.min(b1.y_top_left, b2.y_top_left)
      b1.x_bottom_right = Math.max(b1.x_bottom_right, b2.x_bottom_right)
      b1.y_bottom_right = Math.max(b1.y_bottom_right, b2.y_bottom_right)
      marking.blocks.splice(marking.action_block, 1);
      first_action_block = undefined;
      is_first_click = true;
    }
    
  };
  doc.mousemove.fun = function(x, y){
    drawImage(doc.base_image64);
    action_block(x, y);
    for(var i = 0; i < marking.blocks.length; i++){
      const block = marking.blocks[i];
      if (i == first_action_block){
        drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(0, 255, 0, 0.5)");
      }else if(i == marking.action_block){
        drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(255, 255, 0, 0.5)");
      }else{
        drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(255, 0, 0, 0.5)");
      }
      
    }
    
  };
}


var setSelectDataset = function(){
    $("#tool-select-dataset")[0].innerHTML = "";
    $("#tool-select-dataset")[0].addEventListener('change', function (e) {
        setSelectMarking($("#tool-select-dataset")[0].value);
    });
    const xml = new XMLHttpRequest();
    xml.open("GET", "/dataset/read/");
    xml.send();
    xml.onload = function() {
        if (xml.status == 200) {
            var array =  $.parseJSON(xml.response);
            for(var i=0; i < array.length ; i++){
                var new_elem = $('<option value="'+array[i].id+'">'+array[i].name+'</option>')
                $("#tool-select-dataset").append(new_elem)
            }
            setSelectMarking($("#tool-select-dataset")[0].value);
        }
    }
}

var setSelectMarking= function(dataset_id){
  $("#tool-select-marking")[0].innerHTML = "";
  
    const xml = new XMLHttpRequest();
    xml.open("GET", "/dataset/"+dataset_id+"/markingsegment/read/");
    xml.send();
    marking.markings = {};
    xml.onload = function() {
        if (xml.status == 200) {
            var array =  $.parseJSON(xml.response);
            for(var i=0; i < array.length ; i++){
                var new_elem = $('<option value="'+array[i].id+'">'+array[i].name+'</option>')
                $("#tool-select-marking").append(new_elem)
                marking.markings[array[i].id] = array[i].name
            }
            
        }
    }
}

var markBlock = function(){
    $("#submenu-mark-segment").removeClass("close-submenu");
    setSelectDataset();
    drawImage(doc.base_image64);
    drawSegment(marking.blocks);

    doc.mousedown.fun = function(x, y){
      marking.blocks[marking.action_block].marking_id = $("#tool-select-marking")[0].value;
    };
    doc.mousemove.fun = function(x, y){
      drawImage(doc.base_image64);
      action_block(x, y);
      for(var i = 0; i < marking.blocks.length; i++){
        const block = marking.blocks[i];
        if(i == marking.action_block){
          drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(0, 0, 255, 0.5)");
          drawText(block.x_top_left, block.y_top_left, marking.markings[block.marking_id], pt=tools.font_size, color="rgba(0, 0, 255, 0.5)");
        }else if (block.marking_id == undefined){
          drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(255, 0, 0, 0.5)");
          drawText(block.x_top_left, block.y_top_left, marking.markings[block.marking_id], pt=tools.font_size, color="rgba(255, 0, 0, 0.5)");
        }else{
          drawRectangle(block.x_top_left, block.y_top_left, block.x_bottom_right, block.y_bottom_right, "rgba(0, 255, 0, 0.5)");
          drawText(block.x_top_left, block.y_top_left, marking.markings[block.marking_id], pt=tools.font_size, color="rgba(0, 255, 0, 0.5)");
        }
        
      }
      
    };
}

set_mouse_canvas(canvas);

$("#save-manual-marking-block").click(function(){
    for (var i = 0; i < marking.blocks.length; i++){
        if (marking.blocks[i].marking_id == undefined){
            alert("Не все блоки размечены");
            return;
        }
    }
    for (var i = 0; i < marking.blocks.length; i++){
        const block = marking.blocks[i];
        const xml = new XMLHttpRequest();
        const formData = new FormData();
        block.x_top_left = Math.round(block.x_top_left);
        block.y_top_left = Math.round(block.y_top_left);
        block.x_bottom_right = Math.round(block.x_bottom_right); 
        block.y_bottom_right = Math.round(block.y_bottom_right);
        formData.append('document_id', doc.id);
        formData.append('marking_id', block.marking_id);
        formData.append('json_data', JSON.stringify(block));

        xml.open('POST', '/segmentdata/create/');
        xml.send(formData);
        xml.onload = function() {
            rez = $.parseJSON(xml.response);
            $('#save-alert').addClass('show');
            setTimeout(() => {$("#save-alert").removeClass("show");}, 2000);
        }
    }


})

$("#tool-auto-block").click(function(){
    tools.action = "auto-block";
    close_submenu();
    autoBlock();
})

$("#tool-horizontal-scissors").click(function(){
    tools.action = "horizontal-scissors";
    close_submenu();
    horizontalScissors();
})

$("#tool-vertical-scissors").click(function(){
    tools.action = "vertical-scissors";
    close_submenu();
    verticalScissors();
})

$('#tool-delete-block').click(function(){
    tools.action = "delete-block";
    close_submenu();
    deleteBlock();
})

$('#tool-join-block').click(function(){
    tools.action = "join-block";
    close_submenu();
    joinBlock();
})

$('#tool-mark-block').click(function(){
    tools.action = "mark-block";
    close_submenu();
    markBlock();
})