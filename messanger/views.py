from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages as django_messages


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
def dialogue_page(request, username):
    user_sender = Users.objects.get(username=username)
    user_receiver = request.user
    last_seen = user_sender.activity.get_last_activity
    current_chat = ChatManager.get_or_create_chat(user1=user_receiver, user2=user_sender)
    messages = Chat.get_messages(current_chat)

    context = {
        "messages": messages,
        "user_sender": user_sender,
        "user_receiver": user_receiver,
        "last_seen": last_seen,
    }
    if request.method == "POST":
        message_text = request.POST.get("message")
        photo = request.FILES.get("photo")
        if message_text or photo:
            if message_text and photo:
                Message.objects.create(chat=current_chat, receiver=request.user, sender=user_sender, content=message_text, file=photo)
            elif message_text:
                Message.objects.create(chat=current_chat, receiver=request.user, sender=user_sender, content=message_text)
            else:
                Message.objects.create(chat=current_chat, receiver=request.user, sender=user_sender, file=photo)
            return redirect(reverse("messanger:dialogue", kwargs={"username": username}))
        
        django_messages.warning(request, "You should to send smth don't send empty form")
        return redirect(reverse("messanger:dialogue", kwargs={"username": username}))
    return render(request, "messanger/dialogue_page.html", context=context)
