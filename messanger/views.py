from django.shortcuts import render

def index(request):
    context = {
        "chats": range(10),
    }
    return render(request, "messanger/index.html", context=context)