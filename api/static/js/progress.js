process.list_step = ["image", "tesseract", "graph", "segment", "segment-classifier"]


process.indicator_step = {
    "image": "текущий",
    "tesseract": "",
    "graph": "",
    "segment": "",
    "segment-classifier": "",
}

process.function_step = {
    "image": functionImageStep,
    "tesseract": functionTesseractStep,
    "graph": functionGraphStep,
    "segment": functionSegmentStep,
    "segment-classifier": functionSegmentClassifierStep,
}

process.function_response = {
    "image": functionResponseImage,
    "tesseract": functionResponseTesseract,
    "graph": functionResponseGraph,
    "segment": functionResponseSegment,
    "segment-classifier": functionResponseSegmentClassifier,
}

process.function_start_step = {
    "image": functionStartImageStep,
    "tesseract": functionStartTesseractStep,
    "graph": functionStartGraphStep,
    "segment": functionStartSegmentStep,
    "segment-classifier": functionStartSegmentClassifierStep,
}

process.exist_data_step = {
    "image": false,
    "tesseract": false,
    "graph": false,
    "segment": false,
    "segment-classifier": false,
}

var select = function(name_step) {
    if (process.indicator_step[name_step] != ""){
        var okey = true;
        for(var i = 0; i < process.list_step.length; i++){
            if (process.list_step[i] == name_step) {
                okey = false;
                process.indicator_step[process.list_step[i]] = "текущий"
                process.function_step[name_step]();
            }else{
                if (okey) {
                    process.indicator_step[process.list_step[i]] = "ок"
                } else {
                    if (process.exist_data_step[process.list_step[i]]) {
                        process.indicator_step[process.list_step[i]] = "доступен"
                    }else{
                        process.indicator_step[process.list_step[i]] = ""
                    }

                }
            }

        }

        $(".setting").css("display", "none");
        $("#"+name_step+"-setting").css("display" ,"block");
        process.function_start_step[name_step]();
        drewMenuStep();
    }
}

var unlockStep = function(name_step) {
    process.indicator_step[name_step] = "доступен";
    drewMenuStep();
}

var drewMenuStep = function() {
   for(var i = 0; i < process.list_step.length; i++){
            const st = process.list_step[i];
            const ind = process.indicator_step[st];
            $("#indicator-"+st).text(ind);
            $("#a-indicator-"+st).removeClass("link-warning link-secondary link-primary link-success")
            $("#indicator-"+st).removeClass("bg-warning bg-secondary bg-primary bg-success");
            if (ind == "текущий") {
                $("#a-indicator-"+st).addClass("link-primary");
                $("#indicator-"+st).addClass("bg-primary");
            }else if (ind == "ок") {
                $("#a-indicator-"+st).addClass("link-success");
                $("#indicator-"+st).addClass("bg-success");
            }else if (ind == "") {
                $("#a-indicator-"+st).addClass("link-secondary");
                $("#indicator-"+st).addClass("bg-secondary");
            }else if (ind == "доступен") {
                $("#a-indicator-"+st).addClass("link-warning");
                $("#indicator-"+st).addClass("bg-warning");
            }
        }
}


for(var i = 0; i < process.list_step.length; i++){
    const st = process.list_step[i];
    $("#a-indicator-"+st).click(function(){
        select(st);
    })
}