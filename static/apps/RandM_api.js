$(document).ready(function () {
    $("#generate").click(function (event) {
        $("#spinner").addClass("spinner-border");
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/apps/avatars-RandM/generate/",
            success: function (data) {
                $("#spinner").removeClass("spinner-border");
                $("#result_image").attr("src", data.src);
                $("#name").text(data.name);
                $("#status").text(data.status);
                $("#species").text(data.species);
                $("#gender").text(data.gender);
            },
            error: function (data) {
                console.log(data.message)
            }
        })
    })    
})