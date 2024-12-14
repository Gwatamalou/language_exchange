const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');
const toggleVideoButton = document.getElementById('toggle-video');
const toggleAudioButton = document.getElementById('toggle-audio');
let localStream;

let peerConnection;
const configuration = {
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
};

// Функция для запуска локального видео
async function startLocalVideo() {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        localVideo.srcObject = localStream;
        createPeerConnection();
    } catch (error) {
        console.error("Ошибка доступа к медиа-устройствам:", error);
    }
}

// Создание RTCPeerConnection
function createPeerConnection() {
    peerConnection = new RTCPeerConnection(configuration);

    // Добавление треков локального стрима
    localStream.getTracks().forEach(track => {
        peerConnection.addTrack(track, localStream);
    });

    // Обработка получения удалённого трека
    peerConnection.ontrack = (event) => {
        if (event.streams && event.streams[0]) {
            remoteVideo.srcObject = event.streams[0];
        }
    };

    // Обработка ICE-кандидатов
    peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
            chatSocket.send(JSON.stringify({
                'ice': event.candidate,
                'username': username
            }));
        }
    };
}

// Переключение видео
toggleVideoButton.onclick = () => {
    const videoTrack = localStream.getVideoTracks()[0];
    if (videoTrack) {
        videoTrack.enabled = !videoTrack.enabled;
        toggleVideoButton.classList.toggle('btn-danger');
    }
};

// Переключение аудио
toggleAudioButton.onclick = () => {
    const audioTrack = localStream.getAudioTracks()[0];
    if (audioTrack) {
        audioTrack.enabled = !audioTrack.enabled;
        toggleAudioButton.classList.toggle('btn-danger');
    }
};

// Запуск локального видео при загрузке
startLocalVideo();
