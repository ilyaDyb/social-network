from django.db import models
from django.db.models import Q, Max

from tools import tools_get_timestamp
from users.models import Users

    
class Chat(models.Model):
    participant1 = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="chat_participant1")
    participant2 = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="chat_participant2")

    def __str__(self):
        return f"Chat between {self.participant1} and {self.participant2}"
    
    def get_other_participant(self, user):
        if self.participant1 == user:
            return self.participant2
        else:
            return self.participant1

    def get_messages(self):
        return self.messages.order_by("-timestamp")
    
    def get_last_message(self):
        return self.messages.order_by("-timestamp").first()
    
    
class Message(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="sent_messages", db_index=True)
    receiver = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="received_messages", db_index=True)
    content = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="photo_messages", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        time = self.timestamp.strftime("%H:%M %d.%m")
        return f"Message of {self.sender} to {self.receiver} in {time}"
    
    @staticmethod
    def get_all_chats(receiver_user):
        chats = Message.objects.filter(
            Q(receiver=receiver_user) | Q(sender=receiver_user)
        ).order_by("-timestamp")
        return chats
    
    def get_timestamp(self):
        return tools_get_timestamp(timestamp=self.timestamp)


class ChatManager:
    @staticmethod
    def get_or_create_chat(user1, user2):
        chat = Chat.objects.filter(
            Q(participant1=user1, participant2=user2) | Q(participant1=user2, participant2=user1)
        ).first()
        if not chat:
            chat = Chat.objects.create(participant1=user1, participant2=user2)
        return chat
    
    @staticmethod
    def get_user_chats(user):
        chats = Chat.objects.filter(
            Q(participant1=user) | Q(participant2=user)
        ).annotate(
            last_message_time=Max("messages__timestamp")
        ).order_by("-last_message_time")
        return chats