"use strict";

let protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
let connectionString = `${protocol}://${window.location.host}/ws/notification/`;
let notifySocket = new WebSocket(connectionString);
notifySocket.onmessage = function (event){
    const data = JSON.parse(event.data);
    displayNotification(data.message, data.notify_id);
};

function getCSRFToken() {
    let cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length);
        }
    }
    return '';
}

function displayNotification(message, notify_id) {
    const container = document.getElementById('notification-container');
    const notify = document.createElement('div');
    const buttonContainer = document.createElement('form')
    const csrfInput = document.createElement('input');
    const accept = document.createElement('button')
    const decline = document.createElement('button')


    notify.textContent = message;
    notify.style.padding = '10px';
    notify.style.marginBottom = '10px';
    notify.style.backgroundColor = '#f0f8ff';
    notify.style.border = '1px solid #007bff';
    notify.style.borderRadius = '5px';
    notify.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';

    buttonContainer.method = 'POST';
    buttonContainer.style.display = 'flex';
    buttonContainer.style.justifyContent = 'space-between';
    buttonContainer.style.marginTop = '10px';

    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = getCSRFToken();

    accept.type = 'submit';
    accept.name='accept';
    accept.value=notify_id;
    accept.textContent = "Принять";

    decline.type = 'submit';
    decline.name='decline';
    decline.value=notify_id;
    decline.textContent = "Отклонить";

    buttonContainer.appendChild(csrfInput);
    buttonContainer.appendChild(accept)
    buttonContainer.appendChild(decline)

    notify.appendChild(buttonContainer)
    container.appendChild(notify)



    setTimeout(() => {
        container.removeChild(notify);
    }, 10000);
}