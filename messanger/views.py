import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt


from application import settings
from messanger.models import Chat, ChatManager
from users.models import Users
from tools import photo_validate


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


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        photo = request.FILES['photo']
        validate = photo_validate(photo)
        if validate["status"]:
            filename = photo.name
            file_path = os.path.join(settings.MEDIA_ROOT, 'photo_messages', filename)

            with open(file_path, 'wb+') as destination:
                for chunk in photo.chunks():
                    destination.write(chunk)
            
            file_url = os.path.join(settings.MEDIA_URL, 'photo_messages', filename) #/media/photo_messages/example3.webp

            return JsonResponse({'success': True, 'url': file_url})
        else:
            return JsonResponse({"message": validate["message"]})
    return JsonResponse({'success': False})

@login_required
def dialogue_page(request, username):
    user_sender = Users.objects.get(username=username)
    user_receiver = request.user

    current_chat = ChatManager.get_or_create_chat(user1=user_receiver, user2=user_sender)
    chat_id = current_chat.id

    messages = Chat.get_messages(current_chat)
    is_online, last_activity = user_sender.activity.is_online, user_sender.activity.get_last_activity()

    if last_activity[0] == "0":
        is_online = True

    messages.filter(sender=user_sender).update(is_read=True) #need fix and add this to background task, because a lot of time need for load page

    context = {
        "messages": messages,
        "user_sender": user_sender,
        "user_receiver": user_receiver,
        "is_online": is_online,
        "last_activity": last_activity,
        "chat_id": chat_id,
    }
    return render(request, "messanger/dialogue_page.html", context=context)