document.addEventListener("DOMContentLoaded", function() {
    const messagesContainer = document.getElementById("chat-messages");
    const nextPageInput = document.getElementById("id_nextPage");

    function loadMessages() {
        if (!nextPageInput || isNaN(nextPageInput.value)) return;

        const nextPage = nextPageInput.value;
        const previousScrollHeight = messagesContainer.scrollHeight;
        fetch("?page=" + nextPage, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ page: nextPage })
        })
        .then(response => response.json())
        .then(data => {
            if (data.html) {
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = data.html;
                while (tempDiv.firstChild) {
                    messagesContainer.prepend(tempDiv.firstChild);
                }
            }
            if (data.next_page) {
                nextPageInput.value = data.next_page;
            } else {
                nextPageInput.value = NaN;
            }
            messagesContainer.scrollTop = messagesContainer.scrollHeight - previousScrollHeight;
        })
        .catch(error => console.error('Error:', error));
    }
    messagesContainer.addEventListener('scroll', () => {
        if (messagesContainer.scrollTop === 0) {
            loadMessages();
        }
    });

});