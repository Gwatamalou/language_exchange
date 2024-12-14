const roomName = document.getElementById('chat-box').dataset.roomName;
const username = document.getElementById('chat-log').dataset.username;
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

// Обработка сообщений WebSocket
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.message) {
        const chatLog = document.querySelector('#chat-log');
        const messageElement = document.createElement('div');

        messageElement.className = data.username === username ? 'text-end text-primary' : 'text-start text-secondary';
        messageElement.innerHTML = `<b>${data.username}:</b> ${data.message}`;
        chatLog.append(messageElement);
    }
};

// Отправка сообщения через WebSocket
document.querySelector('#chat-message-submit').onclick = function () {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'username': username,
        'message': message
    }));

    messageInputDom.value = '';
};
