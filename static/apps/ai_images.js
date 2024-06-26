$(document).ready(function () {

    $("#generate_img").click(function name(params) {
        var prompt = $("#prompt").val();
        if (!prompt) {
            alert("You should write prompt");
            return;
        }
        $("#spinner").addClass("spinner-border");
        $.ajax({
            type: "POST",
            url: "http://" + window.location.host + "/apps/ai-images/generate-image/",
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