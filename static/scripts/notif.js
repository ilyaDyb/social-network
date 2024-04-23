var notification = $('#notification');
// И через 7 сек. убираем
if (notification.length > 0) {
    setTimeout(function () {
        notification.alert('close');
    }, 3000);
}