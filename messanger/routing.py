from django.urls import path

from messanger import cosumers


websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/', cosumers.ChatConsumer.as_asgi()),
    path('ws/notifications/<int:user_id>/', cosumers.NotificationConsumer.as_asgi()),
]