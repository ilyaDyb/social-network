document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('upload-photo-btn').addEventListener('click', function() {
        document.getElementById('photo-input').click();
    });
    const chatBlock = document.getElementById("chat-messages");
    chatBlock.scrollTop = chatBlock.scrollHeight;
    
    userReceiverId = document.getElementById("user_receiver_id").value
    const chatId = document.getElementById("chatId").value;
    const userId = document.getElementById("user_receiver_id").value;
    const socket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + chatId + "/");

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const messageElement = document.createElement('div');
        messageElement.innerText = `${data.username}: ${data.message}`;
        document.getElementById('chat-messages').appendChild(messageElement);
    };

    document.getElementById('chat-message-submit').onclick = function() {
        const messageInput = document.getElementById('chat-message-input');
        const message = messageInput.value;
        socket.send(JSON.stringify({
            'message': message,
            'user_id': userId,
            'chat_id': chatId
        }));
        messageInput.value = '';
    };

    document.getElementById('upload-photo-btn').onclick = function() {
        document.getElementById('photo-input').click();
    };

    document.getElementById('photo-input').onchange = function(event) {
        const formData = new FormData();
        formData.append('image', event.target.files[0]);
        formData.append('user_id', userId);
        formData.append('chat_id', chatId);
        fetch('/upload/', {
            method: 'POST',
            body: formData,
        }).then(response => response.json()).then(data => {
            if (data.success) {
                const message = `Sent a photo: ${data.url}`;
                socket.send(JSON.stringify({
                    'message': message,
                    'user_id': userId,
                    'chat_id': chatId
                }));
            }
        });
    };
});