"use strict";

let protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
let connectionString = `${protocol}://${window.location.host}/ws/notification/`;
let notifySocket = new WebSocket(connectionString);
notifySocket.onmessage = function (event){
    const data = JSON.parse(event.data);
    displayNotification(data.message);
};

function displayNotification(message) {
    const container = document.getElementById('notification-container');
    const notify = document.createElement('div');
    notify.textContent = message;
    notify.textContent = message;
    notify.style.padding = '10px';
    notify.style.marginBottom = '10px';
    notify.style.backgroundColor = '#f0f8ff';
    notify.style.border = '1px solid #007bff';
    notify.style.borderRadius = '5px';
    notify.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';

    container.appendChild(notify)

    setTimeout(() => {
        container.removeChild(notify);
    }, 10000);
}