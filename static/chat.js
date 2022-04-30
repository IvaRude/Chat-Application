const user_username = JSON.parse(document.getElementById('user_username').textContent);
const roomName = JSON.parse(document.getElementById('chat_pk').textContent);

// document.querySelector('#input').onkeyup = function(e) {
//     if (e.keyCode === 13) {  // enter, return
//         document.querySelector('#submit').click();
//     }
// };

document.querySelector('#input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#submit').click();
    }
};

document.querySelector('#submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'content': message,
        'author': user_username,
        'command': 'new_message',
        // 'command': 'fetch_messages',
        // 'chat_name': roomName,
    }));
    messageInputDom.value = '';
};
// Непонятно, как правильно... И так, и так работает
// const chatSocket = new WebSocket(
const chatSocket = new ReconnectingWebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    roomName +
    '/'
);

chatSocket.onopen = function(e) {
    fetchMessages();
}

function fetchMessages() {
    chatSocket.send(JSON.stringify({'command': 'fetch_messages' }));
}

// chatSocket.onmessage = function (e) {
//     const data = JSON.parse(e.data);
//     console.log(data)
//     document.querySelector('#chat-text').value += (data.username + ': ' + data.message + '\n')
// }   

chatSocket.onmessage = function(e) {
var data = JSON.parse(e.data);
console.log(data)
if (data['command'] === 'fetch_messages') {
    for (let i=data['messages'].length - 1; i >= 0; i--) {
    createMessage(data['messages'][i]);
    }
} else if (data['command'] === 'new_message'){
    createMessage(data['message']);
}

function createMessage(data) {
    // console.log(data)
    var author = data['author'];
    var pTag = document.createElement('p');
    pTag.textContent = author + ': ' + data.content;
    document.querySelector('#chat-text').appendChild(pTag);
}
};