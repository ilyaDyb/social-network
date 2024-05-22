$(document).ready(function () {
    $(".likeBtn").click(function () {
        var newImage = $(this).data("heart-after");
        $(this).attr("src", newImage);
    });

    var hasNextPage = $("#nextPage").val() !== "None";

    function loadMorePosts() {
        var nextPage = parseInt($("#nextPage").val());
        console.log(nextPage)
        if (hasNextPage) {
            $.ajax({
                url: "http://127.0.0.1:8000/feed/?page=" + nextPage,
                type: 'POST',
                success: function (data) {
                    $("#posts-block").append(data.html);
                    if (data.html.trim() === "") {
                        hasNextPage = false;
                    } else {
                        nextPage++;
                        $("#nextPage").val(nextPage);
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Ошибка при загрузке постов:', error);
                    hasNextPage = false;
                }
            });
        }
    }

    $(window).scroll(function() {
        if ($(window).scrollTop() + $(window).height() >= $(document).height()) {
            loadMorePosts();
        };
    });
});
