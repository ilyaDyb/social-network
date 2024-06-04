$(document).ready(function () {
    var cnt = 0;
    $(".likeBtn").click(function () {
        var postId = $(this).data("post-id")
        if (cnt % 2 === 0) {
            $(this).attr("src", "/static/images/heart_after.png");
        }
        else if (cnt % 2 === 1) {
            $(this).attr("src", "/static/images/heart_before.png");
        };
        cnt++
        $.ajax({
            url: "http://" + window.location.host + "/like-post/",
            type: "POST",
            data: { post_id : postId },
            success: function (data) {
                likeId = "#likes-" + postId;
                var likes = parseInt($(likeId).text());
                if (data.status === "liked"){
                    likes++;
                    $(likeId).text(likes);
                }
                else if (data.status === "unliked"){
                    likes--;
                    $(likeId).text(likes);
                }
            },
            error: function (data) {
                console.log("error")
            }
        });
    });

    var hasNextPage = $("#nextPage").val() !== "None";

    function loadMorePosts() {
        var nextPage = parseInt($("#nextPage").val());
        console.log(nextPage)
        if (hasNextPage) {
            $.ajax({
                url: "http://" + window.location.host + "/feed/?page=" + nextPage,
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
