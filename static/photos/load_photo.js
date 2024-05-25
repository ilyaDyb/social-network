const fileInput = $("#fileInput");
var successMessage = $("#jq-notification");
const uploadBtn = $("#uploadBtn");

uploadBtn.on('click', function() {
    fileInput.click();
});

fileInput.on('change', function() {
    const file = this.files[0];

    if (file) {
        const formData = new FormData();
        formData.append("file", file);

        $.ajax({
            type: "POST",
            url: "http://" + window.location.host + "/photos/load-photo/",
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
            },
            error: function(xhr, status, error) {
                console.log("Error:", error);
            }
        });
    }
});
