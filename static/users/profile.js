var successMessage = document.getElementById("jq-notification");
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
                console.log("success")
            },
            error: function(data) {
                console.log("Error")
            }
        });
        document.getElementById('previewImg').src = imageUrl;
    }
});