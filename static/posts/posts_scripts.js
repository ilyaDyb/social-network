$(document).ready(function () {
    $(".likeBtn").click(function () {
        var postId = $(this).data("post-id");
        var likeId = "#likes-" + postId;
        var heartBeforeUrl = "/static/images/heart_before.png";
        var heartAfterUrl = "/static/images/heart_after.png";
        var $this = $(this);
        $.ajax({
            url: "/like-post/",
            type: "POST",
            data: {
                post_id: postId,
            },
            success: function (data) {
                var likes = parseInt($(likeId).text());
                if (data.status === "liked") {
                    likes++;
                    $this.attr("src", heartAfterUrl);
                    $(likeId).text(likes);
                } else if (data.status === "unliked") {
                    likes--;
                    $this.attr("src", heartBeforeUrl);
                    $(likeId).text(likes);
                }
            },
            error: function (data) {
                console.log("error");
            }
        });
    });

    var hasNextPage = $("#nextPage").val() !== "None";

    function loadMorePosts() {
        var nextPage = parseInt($("#nextPage").val());
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
    $(".sendCommentBtn").click(function () {
        var postId = $(this).data("post-id");
        var commentText = $(this).prevAll(".commentText").val();
        $.ajax({
            url: "/write-comment/",
            type: "POST",
            data: { post_id : postId, comment_text : commentText},
            success: function (data) {
                $("#post-comments_" + postId).append(data.html);
            },
            error: function (error) {
                console.error(error)
            }
        })
    });
    var cnt = 0
    $(".comments-btn").click(function (event) {
        postId = $(this).data("post-id");
        if (cnt === 0) {     
            $.ajax({
                url: "/show-comments/",
                type: "POST",
                data: { post_id : postId },
                success: function (data) {
                    $("#post-comments_" + postId).append(data.html);
                    cnt++;
                },
                error: function (data) {
                   console.log("Error") ;
                },
            });
        };
    });
});
