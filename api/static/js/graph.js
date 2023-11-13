$("#a-indicator-graph").click(function(){
    if (!$("#a-indicator-graph")[0].classList.contains("link-secondary")) {
        $(".setting").css("display", "none");
        $("#graph-setting").css("display" ,"block");
        $("#indicator-graph").text("Текущий");
        $("#a-indicator-graph").removeClass("link-warning")
        $("#a-indicator-graph").addClass("link-primary");
    }
})