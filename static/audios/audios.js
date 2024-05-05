document.addEventListener("DOMContentLoaded", function() { 
    var audioElements = document.querySelectorAll('audio');
    
    var successMessage = $("#jq-notification");
    
    audioElements.forEach(audio => {
        audio.addEventListener('play', () => {
            audioElements.forEach(element => {
                if (element !== audio) {
                    element.pause();
                    element.currentTime = 0;
                }
            });
        });
    });
    audioElements.forEach((audio, index) => {
        audio.addEventListener('ended', () => {
            const nextAudio = audioElements[index + 1];
            if (nextAudio) {
                nextAudio.play();
            }
        });
    });
    
    
    const volumeSlider = document.querySelector('.volume-slider');

    volumeSlider.addEventListener('input', () => {
        const volume = parseFloat(volumeSlider.value);
        audioElements.forEach(audio => {
            audio.volume = volume;
        });
    });

    $(".add-audio").click(function (event) {
       var audioId = $(this).data("audio-id");
       $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/audios/add-audio/",
        data: {audioId: audioId},
        success: function(data) {
            successMessage.html(data.message);
            successMessage.fadeIn(400);
            setTimeout(function () {
                successMessage.fadeOut(400);
            }, 7000);
        },
        error: function(xhr, status, error) {
            console.error("Error adding audio :", error);
        },
    
       });
    });
    
    // $(".delete-audio").click(function (event) {
    //    var audioId = $(this).data("audio-id");
    //    $.ajax({
    //     type: "POST",
    //     url: "http://127.0.0.1:8000/audios/delete-audio/",
    //     data: {audioId: audioId},
    //     success: function(data) {
    //         successMessage.html(data.message);
    //         successMessage.fadeIn(400);
    //         setTimeout(function () {
    //             successMessage.fadeOut(400);
    //         }, 7000);
    //     },
    //     error: function(xhr, status, error) {
    //         console.error("Error adding audio :", error);
    //     },
    
    //    });
    // });
});