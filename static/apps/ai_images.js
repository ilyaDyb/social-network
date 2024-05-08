$(document).ready(function () {

    $("#generate_img").click(function name(params) {
        var prompt = $("#prompt").val();
        if (!prompt) {
            alert("You should to write prompt");
            return;
        }
        $("#spinner").addClass("spinner-border");
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/apps/ai-images/generate-image/",
            data: {prompt: prompt},
            success: function (data) {
                $("#spinner").removeClass("spinner-border");
                $("#result_image").attr("src", data.image);
            },
            error: function (data) {
                console.log(data.message)
            }
        });
    });
});