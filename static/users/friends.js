$(document).ready(function() {
    $("#showBlock").click(function(event) {
        event.preventDefault();
        $("#hiddenBlock").toggle();
    });
    
    $("#acceptRequest").click(function(event) {
        event.preventDefault();
        
        var successMessage = $("#jq-notification");
        var url = $(this).attr("href");
        console.log(url);
        $.ajax({
            type: "POST",
            url: url,
            data: {csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),},
            success: function(data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
            },
            error: function(data) {
                console.log("error");
            }
        });
    });
});
    