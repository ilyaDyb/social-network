import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chat
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message = data.get('message')
        user_id = data.get('user_id')
        chat_id = data.get('chat_id')
        file_url = data.get('file_url')

        if message or file_url:
            user = await sync_to_async(User.objects.get)(id=user_id)
            await self.save_message(user, chat_id, message, file_url)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username,
                    'file_url': file_url,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        file_url = event['file_url']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'file_url': file_url,
        }))

    @sync_to_async
    def save_message(self, user, chat_id, content, file_url):
        chat = Chat.objects.get(id=chat_id)
        other_user = Chat.get_other_participant(chat, user=user)
        Message.objects.create(sender=user, receiver=other_user, chat=chat, content=content, file=file_url)