const marking = {}

var createManualMarking = function (){
    const blocks_json = JSON.stringify(marking.blocks);
    console.log(blocks_json);
}

$("#save-manual-marking-block").click(function(){
    createManualMarking();
})