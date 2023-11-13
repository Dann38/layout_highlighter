$("#a-indicator-graph").click(function(){
    if (!$("#a-indicator-graph")[0].classList.contains("link-secondary")) {
        $(".setting").css("display", "none");
        $("#graph-setting").css("display" ,"block");
        $("#indicator-graph").text("Текущий");
        $("#a-indicator-graph").removeClass("link-warning")
        $("#a-indicator-graph").addClass("link-primary");
    }
})

$("#button_graph").click(function(){

    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    const bboxes = process.bboxes;

    formData.append('bboxes', JSON.stringify(bboxes));

    xhr.open('POST', '/graph_process');
    xhr.send(formData);

    xhr.onload = function() {
        if (xhr.status != 200) {
          alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            var response_bboxes = $.parseJSON(xhr.response);
            const points = response_bboxes.list_point;
            process.points = points;
            for(var i = 0; i < points.length; i++){
                const point = points[i];
                writePoint(point.x, point.y);
            }
            changeIndicatorPoint();

        }
    };
});

var changeIndicatorPoint = function(){
    $("#a-indicator-graph").removeClass("link-primary");
    $("#a-indicator-graph").addClass("link-success");
    $("#indicator-graph").text("OK");
    $("#indicator-graph").removeClass("bg-primary");
    $("#indicator-graph").addClass("bg-success");
//    $("#a-indicator-segment").removeClass("link-secondary");
//    $("#a-indicator-segment").addClass("link-warning");
}