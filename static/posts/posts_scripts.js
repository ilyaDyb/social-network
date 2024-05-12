$(document).ready(function () {
    $(".likeBtn").click(function () {
        newImage = $(this).data("heart-after");
        $(this).attr("src", newImage);
    })
})