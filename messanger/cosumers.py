import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

from users.models import Users
# from webpush import send_user_notification

from .models import Message, Chat

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

    async def disconnect(self):
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
            user = await self.get_user(user_id)
            chat = await self.get_chat(chat_id)
            other_user = await self.get_other_user(chat, user)
            other_user_activity = await self.get_status(user=other_user)

            await self.save_message(user, chat, other_user, message, str(file_url)[6:])

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username,
                    'file_url': file_url,
                }
            )

            if other_user_activity:
                print(f"Sending notification to user_{other_user.id}_notifications")
                await self.channel_layer.group_send(
                    f"user_{other_user.id}_notifications",
                    {
                        "type": "notification_message",
                        "message": message if message else "You have received a new file.",
                        "chat_id": chat_id,
                        "user_id": user_id
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

    @database_sync_to_async
    def get_status(self, user):
        if user.activity.get_last_activity()[0] == "0":
            return True
        return user.activity.is_online
    
    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_chat(self, chat_id):
        return Chat.objects.get(id=chat_id)

    @database_sync_to_async
    def get_other_user(self, chat, user):
        return Chat.get_other_participant(chat, user=user)

    @database_sync_to_async
    def save_message(self, user, chat, other_user, content, file_url):
        Message.objects.create(sender=user, receiver=other_user, chat=chat, content=content, file=file_url)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = f"user_{self.user_id}_notifications"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

        print(f"User {self.user_id} connected to notifications")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        print(f"User {self.user_id} disconnected from notifications")

    async def notification_message(self, event):
        print(f"Notification for user {self.user_id}: {event}")
        message = event["message"]
        chat_id = event["chat_id"]
        user_id = event["user_id"]
        user_data  = await self.get_data_about_user(user_id)
        await self.send(text_data=json.dumps({
            'message': f"{message[:30]}...",
            'chat_id': chat_id,
            'user_data': user_data,
        }))

    @database_sync_to_async
    def get_data_about_user(self, user_id):
        try:
            user_obj = Users.objects.get(pk=user_id)
            user_data = {
                "username": user_obj.username,
                "first_name": user_obj.first_name,
                "last_name": user_obj.last_name,
            }
            return user_data
        except Exception as ex:
            print(ex)
            return None