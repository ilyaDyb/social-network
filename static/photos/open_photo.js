$(document).ready(function() {
    var modal = $("#photoModal");
    var modalImg = $("#modalPhoto");
    var closeModalBtn = $(".close-modal");
    var deletePhotoBtn = $(".delete-photo-btn");
    var photoId = null;
    
    $(document).on('click', '.post-photo', function () {
        var imageUrl = $(this).attr("src");
        $("#modalPostImg").attr("src", imageUrl);
        $("#modalPost").show();
    });

    $(".photo-link").click(function(event) {
        event.preventDefault();
        var imageUrl = $(this).data("image");
        photoId = $(this).data("photo-id");
        modalImg.attr("src", imageUrl);
        modal.show();
    });

    closeModalBtn.click(function() {
        modal.hide();
        $("#modalPost").hide();
    });

    deletePhotoBtn.click(function() {
        if (photoId) {
            $.ajax({
                type: "POST",
                url: "http://" + window.location.host + "/photos/delete/",
                data: { photo_id: photoId },
                success: function(data) {
                    modal.hide();
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
