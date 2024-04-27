var successMessage = $("#jq-notification");
// Находим элементы кнопки и input
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
            url: "http://127.0.0.1:8000/users/profile/edit-img/",
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
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
        document.getElementById('previewImg').src = imageUrl;
    }
});

$(document).ready(function() {
    $("#showBlock").click(function() {
        $("#hiddenBlock").toggle();
    });
    $("#saveButton").click(function(){
        text = $("#textInput").val();
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/users/profile/edit-short-inf/",
            data: {"text": text},
            success: function(data) {
                $("#shortInf").text(text)
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