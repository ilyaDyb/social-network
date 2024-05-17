$(document).ready(function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const captchaResponse = grecaptcha.getResponse();
        if (!captchaResponse) {
            $("#warning").text("You should complete the captcha.")
            throw new Error("Captcha not completed");
        } else {
            form.submit();
        }
    });
});