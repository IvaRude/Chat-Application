user_username = JSON.parse(document.getElementById('user_username').textContent);
roomName = JSON.parse(document.getElementById('chat_pk').textContent);
var page = 1;


document.querySelector('.write_msg').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('.msg_send_btn').click();
    }
};


document.querySelector('.msg_send_btn').onclick = function (e) {
    const messageInputDom = document.querySelector('.write_msg');
    const message = messageInputDom.value;
    if(message.length == 0) {
        return 
    }
    chatSocket.send(JSON.stringify({
        'content': message,
        'author': user_username,
        'command': 'new_message',
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
    
    fetchMessages(page);
};


function fetchMessages(page) {
    chatSocket.send(JSON.stringify({'command': 'fetch_messages',
                                    'page': page }));
};


chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    console.log(data)
    if (data['command'] === 'fetch_messages') {
        for (let i=0; i < data['messages'].length; i++) {
            var msg = createMessage(data['messages'][i]);
            document.querySelector('.msg_history').prepend(msg);
        }
    } else if (data['command'] === 'new_message'){
        var msg = createMessage(data['message']);
        document.querySelector('.msg_history').appendChild(msg);
        $(".msg_history").scrollTop(123);
    }
};

function createMessage(data) {
    var author = data['author'];

    var message = document.createElement('p');
        message.textContent = data['content'];

        var date = document.createElement('span');
        date.className = 'time_date';
        date.textContent = data['timestamp'];

    if(username === author){
        var div1 = document.createElement('div');
        div1.className = 'outgoing_msg';

        var div2 = document.createElement('div');
        div2.className = 'sent_msg';

        div2.appendChild(message);
        div2.appendChild(date);
        div1.appendChild(div2);
        return div1;
    }
    else {
        var div1 = document.createElement('div');
        div1.className = 'incoming_msg';

        var div2 = document.createElement('div');
        div2.className = 'incoming_msg_img';

        var avatar = document.createElement('img');
        avatar.src = data['avatar'];
        avatar.alt = 'sunil';

        var div3 = document.createElement('div');
        div3.className = 'received_msg';

        var div4 = document.createElement('div');
        div4.className = 'received_withd_msg';

        div4.appendChild(message);
        div4.appendChild(date);

        div3.appendChild(div4);
        div2.appendChild(avatar);
        div1.append(div2);
        div1.append(div3);
        return div1;
    }
};


var chat = $('#chat');
// $(window).scroll(function()
chat.scrollTop(chat[0].scrollHeight);
// chat.scrollIntoView({ behavior: 'smooth', block: 'end' });
$(".msg_history").scrollTop($(".msg_history")[0].scrollHeight);
chat.scroll(function(){
        if ($(this).scrollTop() == 0) {
            page += 1;
            fetchMessages(page);
            // var h = $(chat).children().eq(0).height();
            var h = 1;
            chat.scrollTop(2);
            console.log(chat.scrollHeight);
        }
    });