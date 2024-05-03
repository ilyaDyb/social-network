$(document).ready(function() {
    var modal = $("#photoModal");
    var modalImg = $("#modalPhoto");
    var closeModalBtn = $(".close-modal");
    var deletePhotoBtn = $(".delete-photo-btn");
    var photoId = null;

    $(".photo-link").click(function(event) {
        event.preventDefault();
        var imageUrl = $(this).data("image");
        photoId = $(this).data("photo-id"); // Сохраняем ID фотографии
        modalImg.attr("src", imageUrl);
        modal.show();
    });

    closeModalBtn.click(function() {
        modal.hide();
    });

    deletePhotoBtn.click(function() {
        console.log("click")
        if (photoId) {
            console.log("if")
            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:8000/photos/delete/", // Укажите URL для удаления фотографии по ID на сервере
                data: { photo_id: photoId }, // Отправляем ID фотографии на сервер
                success: function(data) {
                    modal.hide(); // Скрыть модальное окно после успешного удаления
                    alert("Photo deleted successfully.");
                },
                error: function(xhr, status, error) {
                    console.error("Error deleting photo:", error);
                }
            });
        } else {
            console.error("No photo ID available.");
        }
    });
});
