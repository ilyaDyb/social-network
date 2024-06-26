var successMessage = $("#jq-notification");
const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');

uploadBtn.addEventListener('click', function() {
    fileInput.click();
});

fileInput.addEventListener('change', function() {

    const file = this.files[0];

    if (file) {

        const imageUrl = URL.createObjectURL(file);
        var formData = new FormData();
        formData.append("file", file);
        $.ajax({
            type: "POST",
            url: "http://" + window.location.host + "/profile/edit-img/",
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.message != "Your file is too big") {
                    document.getElementById('previewImg').src = imageUrl;
                }
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
            },
            error: function(data) {
                console.log("Error")
            }
        });
    }
});

$(document).ready(function() {
    $("#showBlock").click(function() {
        $("#hiddenBlock").toggle();
    });
    $("#saveButton").click(function(){
        var text = $("#textInput").val();
        $.ajax({
            type: "POST",
            url: "http://" + window.location.host + "/profile/edit-short-inf/",
            data: {"text": text},
            success: function(data) {
                if (data.message != "Your text is too big") {
                    $("#shortInf").text(text) 
                }
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
            },
            error: function(data) {
                console.log("Error")
            }
        });
    });
});
$(document).ready(function() {
    $("#sendRequest").click(function(event) {
        event.preventDefault();

        var url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: url,
            data: {},
            success: function(data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("Error:", textStatus, errorThrown);
            }
        });
    });
});

$(document).ready(function() {
    $(document).on("click", "#btnDelPost", function() {
        var postId = $(this).data("post-id");
        
        $.ajax({
            type: "POST",
            url: "http://" + window.location.host + "/delete-post/",
            data: {post_id: postId},
            success: function(data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
                var divId = "#post_" + postId;
                $(divId).remove();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("Error:", textStatus, errorThrown);
            }
        });
    });
});
