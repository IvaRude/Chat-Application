var username = JSON.parse(document.getElementById('user_username').textContent);
var roomName = JSON.parse(document.getElementById('chat_pk').textContent);
if(username) {
    var sidebarSocket = new ReconnectingWebSocket(
        'ws://' +
        window.location.host +
        '/ws/user/' +
        username +
        '/'
    );
};


sidebarSocket.onopen = function(e) {
    fetchChats();
}


function fetchChats() {
    console.log('fetchChats');
    sidebarSocket.send(JSON.stringify({'command': 'fetch_chats' }));
}


sidebarSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    console.log(data)
    if (data['command'] === 'fetch_chats') {
        
        document.querySelector('#sidebar').innerHTML = "";

        for (let i=data['chats'].length - 1; i >= 0; i--) {
        createChatLink(data['chats'][i]);
        }
    } else if (data['command'] === 'search'){
        document.querySelector('#sidebar').innerHTML = "";
        if(data['users'].length > 0) {
            for (let i=data['users'].length - 1; i >= 0; i--) {
            createUserLink(data['users'][i]);
            }
        }
        else {
            var p = document.createElement('p')
            p.textContent = 'Users not found';
            p.className = 'no_users';
            document.querySelector('#sidebar').appendChild(p);
        }
    }
};


function createUserLink(data) {
    var title = data['title'];
    var user_pk = data['pk'];

    var aTag = document.createElement('a');
    aTag.href = data['link'];
    aTag.className = 'chat_link'
    var div1 = document.createElement('div');
    div1.className = 'chat_list';
    if (roomName && roomName == data['chat_pk']){
        div1.className += ' active_chat';
    }
    var div2 = document.createElement('div');
    div2.className = 'chat_people';
    var div3 = document.createElement('div');
    var div4 = document.createElement('div');
    var img = document.createElement('img');
    img.alt = 'sunil';
    img.src = data['avatar'];
    div3.appendChild(img);
    div3.className = 'chat_img';
    div4.className = 'chat_ib';
    var name = document.createElement('h5');
    name.textContent = data['title'];
    div4.appendChild(name);
    div2.appendChild(div3);
    div2.appendChild(div4);
    div1.appendChild(div2);
    aTag.appendChild(div1);
    document.querySelector('#sidebar').appendChild(aTag);
}


function createChatLink(data) {
    var title = data['title'];
    var last_message = data['last_message'];
    var link = data['link'];

    var aTag = document.createElement('a');
    aTag.href = link;
    aTag.className = 'chat_link'

    var div1 = document.createElement('div');
    div1.className = 'chat_list';
    if (roomName && roomName == data['chat_pk']){
        div1.className += ' active_chat';
    }
    var div2 = document.createElement('div');
    div2.className = 'chat_people';
    var div3 = document.createElement('div');
    var div4 = document.createElement('div');
    var img = document.createElement('img');
    img.alt = 'sunil';
    img.src = data['avatar'];
    div3.appendChild(img);
    div3.className = 'chat_img';
    div4.className = 'chat_ib';
    var name = document.createElement('h5');
    name.textContent = data['title'];
    var date = document.createElement('span');
    date.className = 'chat_date';
    date.textContent = data['timestamp'];
    name.appendChild(date);
    var message = document.createElement('p');
    message.textContent = last_message;
    div4.appendChild(name);
    div4.appendChild(message);
    div2.appendChild(div3);
    div2.appendChild(div4);
    div1.appendChild(div2);
    aTag.appendChild(div1);
    document.querySelector('#sidebar').appendChild(aTag);
};


document.querySelector('.search-bar').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#search_btn').click();
    }
};


document.querySelector('#search_btn').onclick = function (e) {
    if(username){
    const inputSearch = document.querySelector('.search-bar');
    const search = inputSearch.value;
    sidebarSocket.send(JSON.stringify({
        'search': search,
        'command': 'search',
    }));
    inputSearch.value = '';
}};


document.querySelector('#contacts').onclick = function (e) {
    if(username){
    const inputSearch = document.querySelector('.search-bar');
    fetchChats();
    inputSearch.value = '';
}};