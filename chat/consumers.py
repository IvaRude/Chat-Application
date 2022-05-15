# from contextlib import AsyncContextDecorator
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
import json
import websockets
import asyncio

from .models import Message, Chat

User = get_user_model()

class ChatRoomConsumer(AsyncWebsocketConsumer):
    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp),
        }

    async def messages_to_json(self, messages):
        return [await sync_to_async(self.message_to_json)(message) for message in messages]

    async def fetch_messages(self, data):
        page = data['page']
        messages = await sync_to_async(list)(self.chat.get_page(int(page)))
        content = {
            'messages': await self.messages_to_json(messages),
            'command': 'fetch_messages',
        }
        await self.send_messages(content)

    async def new_message(self, data):
        author = data['author']       
        author_user = await sync_to_async(lambda: list(User.objects.filter(username=author))[0])()
        message = await sync_to_async(Message.objects.create)(
            chat=self.chat,
            author=author_user,
            content = data['content'])
        content = {
            'command': 'new_message',
            'message': await sync_to_async(self.message_to_json)(message),
        }
        # Иначе другие пользователи не увидят новое сообщение без обновления страницы!
        await self.send_chat_message(content)

        tasks = []
        members = await sync_to_async(list)(message.chat.members.all())
        for member in members:
            task = asyncio.create_task(self.channel_layer.group_send('sidebar_%s' % member.username,
            {
                'type': 'fetch_chats',
            }))
            tasks.append(task)
            # await self.channel_layer.group_send('sidebar_%s' % member.username,
            # {
            #     'type': 'fetch_chats',
            # })
        asyncio.as_completed(tasks)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    async def connect(self):
        self.chat_pk = self.scope['url_route']['kwargs']['chat_pk']
        self.chat = await sync_to_async(Chat.objects.get)(pk=self.chat_pk)
        self.room_group_name = 'chat_%s' % self.chat_pk
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Должно быть перед сообщениями!
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.commands[text_data_json['command']](self, text_data_json)
    
    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                # type указывает на нужный метод
                'type': 'chatroom_message',
                'message': message,
                # 'username': username,
            }
        )
    
    async def send_messages(self, messages):
        await self.send(text_data=json.dumps(messages))

    async def chatroom_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))


class SideBarConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.user = await sync_to_async(User.objects.get)(username=self.username)
        self.sidebar_name = 'sidebar_%s' % self.username
        
        await self.channel_layer.group_add(
            self.sidebar_name,
            self.channel_name
        )
        # Должно быть перед сообщениями!
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.sidebar_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.commands[text_data_json['command']](self, text_data_json)

    def one_chat_to_json(self, chat):
        title = chat.members.exclude(pk=self.user.pk)[0].username
        last_message = chat.last_message().content
        # link = chat.get_absolute_url()
        if len(last_message) > 15:
            last_message = last_message[:12] + '...'
        return {
            'title': title,
            'last_message': last_message,
            'chat_pk': chat.pk,
            'link': chat.get_absolute_url(),
            # 'timestamp': str(message.timestamp),
        }

    async def chats_to_json(self, chats):
        # return await self.one_chat_to_json(chats[0])
        return [await sync_to_async(self.one_chat_to_json)(chat) for chat in chats]
    
    async def fetch_chats(self, data):
        # await sync_to_async(print)('fetch_chats')
        chats = await sync_to_async(list)(self.user.chats.filter(is_empty=False).order_by('timestamp'))
        content = {
            'chats': await self.chats_to_json(chats),
            'command': 'fetch_chats',
        }
        await self.send_chats(content)
    
    
    commands = {
        'fetch_chats': fetch_chats,
        # 'new_message': new_message,
    }

    async def send_chats(self, chats):
        await self.send(text_data=json.dumps(chats))