document.querySelector('#end-chat').onclick = function () {
    window.location.href = "{% url 'ads_list' 'all' %}";
};

async function handleSDP(sdp) {
    try {
        await peerConnection.setRemoteDescription(new RTCSessionDescription(sdp));
        if (sdp.type === 'offer') {
            const answer = await peerConnection.createAnswer();
            await peerConnection.setLocalDescription(answer);
            chatSocket.send(JSON.stringify({
                'sdp': answer,
                'username': username
            }));
        }
    } catch (error) {
        console.error("Ошибка обработки SDP:", error);
    }
}


async function handleICE(ice) {
    try {
        await peerConnection.addIceCandidate(new RTCIceCandidate(ice));
    } catch (error) {
        console.error("Ошибка добавления ICE-кандидата:", error);
    }
}
