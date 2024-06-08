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
                url: "/feed/?page=" + nextPage,
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
    $(document).on("click", ".sendCommentBtn", function () {
        event.preventDefault();

        var $this = $(this);
        var postId = $this.data("post-id");
        var commentText = $this.siblings(".commentText").val();
        var fileInput = $this.siblings("input[type='file']")[0];
        var file = fileInput.files[0];

        if (!commentText && !file) {
            alert("Write a comment or choose file please");
            return;
        }

        var formData = new FormData();
        formData.append("post_id", postId);
        formData.append("comment_text", commentText);
        if (file) {
            formData.append("file", file);
        }
        $.ajax({
            url: "/write-comment/",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                $("#post-comments_" + postId).append(data.html);
            },
            error: function (error) {
                console.error(error)
            }
        })
    });
    $(".comments-btn").click(function (event) {
        var $this = $(this);
        var postId = $this.data("post-id");
        var cnt = $this.data("cnt");

        if (cnt === 0) {
            $.ajax({
                url: "/show-comments/",
                type: "POST",
                data: { post_id: postId },
                success: function (data) {
                    $("#post-comments_" + postId).append(data.html);
                    cnt++;
                    $this.data("cnt", cnt);
                },
                error: function (data) {
                    console.log("Error");
                },
            });
        } else if (cnt % 2 === 1) {
            $("#post-comments_" + postId).hide();
            cnt++;
            $this.data("cnt", cnt);
        } else if (cnt % 2 === 0) {
            $("#post-comments_" + postId).show();
            cnt++;
            $this.data("cnt", cnt);
        }
    });
});
