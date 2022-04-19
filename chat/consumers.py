from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
import json

from .models import Message

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
        messages = await sync_to_async(list)(Message.objects.order_by('-timestamp').all()[:10])
        content = {
            'messages': await self.messages_to_json(messages),
            'command': 'fetch_messages',
        }
        await self.send_message(content)

    async def new_message(self, data):
        author = data['author']       
        author_user = await sync_to_async(lambda: list(User.objects.filter(username=author))[0])()
        message = await sync_to_async(Message.objects.create)(
            author=author_user,
            content = data['content'])
        content = {
            'command': 'new_message',
            'message': await sync_to_async(self.message_to_json)(message),
        }
        # Иначе другие пользователи не увидят новое сообщение без обновления страницы!
        await self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
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
    
    async def send_message(self, messages):
        await self.send(text_data=json.dumps(messages))

    async def chatroom_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))