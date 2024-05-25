from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages as django_messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from messanger.models import Chat, ChatManager, Message
from users.models import Users


@login_required
def chats_page(request):
    user = request.user
    chats = ChatManager.get_user_chats(user=user)
    chat_details = []

    for chat in chats:
        other_participant = chat.get_other_participant(user=user)
        last_message = chat.get_last_message()
        chat_details.append({
            "other_participant": other_participant,
            "last_message": last_message,
        })

    context = {
        "chat_details": chat_details,
    }

    return render(request, "messanger/chats_page.html", context=context)

@login_required
@csrf_exempt
def upload_photo(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        chat_id = request.POST.get('chat_id')
        photo = request.FILES.get('photo')

        if user_id and chat_id and photo:
            user = Users.objects.get(id=user_id)
            chat = Chat.objects.get(id=chat_id)
            other_user = Chat.get_other_participant(chat, user)
            message = Message.objects.create(sender=user, receiver=other_user, chat=chat, file=photo)
            return JsonResponse({'success': True, 'url': message.file.url})
    
    return JsonResponse({'success': False})

@login_required
def dialogue_page(request, username):
    user_sender = Users.objects.get(username=username)
    user_receiver = request.user
    user_activity = user_sender.activity

    current_chat = ChatManager.get_or_create_chat(user1=user_receiver, user2=user_sender)
    chat_id = current_chat.id

    messages = Chat.get_messages(current_chat)

    context = {
        "messages": messages,
        "user_sender": user_sender,
        "user_receiver": user_receiver,
        "user_activity": user_activity,
        "chat_id": chat_id,
    }
    return render(request, "messanger/dialogue_page.html", context=context)