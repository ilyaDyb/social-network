from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from users.models import Users

from .models import Audio, UserAudio
from .forms import AudioForm


def audios(request, username):
    try:
        user = Users.objects.get(username=username)
    except Users.DoesNotExist:
        return HttpResponse(status=404)
    
    search = request.GET.get("search")
    audios = None

    if search:
        audios = Audio.objects.filter(Q(title__icontains=search) | Q(author__icontains=search))
        flag = "search"

    if not search:
        audios = UserAudio.objects.filter(user=user)
        flag = "not_search"

    context = {
        "username": username,
        "audios": audios,
        "flag": flag,
    }
    return render(request, "audios/audios.html", context=context)


@login_required
def load_audio(request):
    if request.method == "POST":
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            author = form.cleaned_data.get("author")
            audio_file = form.cleaned_data.get("audio_file")
            if audio_file.size > 5 * 1024 * 1024:
                messages.warning(request, "Your audio file is too big")
            if audio_file.name.endswith(".mp3"):
                Audio.objects.create(title=title, author=author, audio_file=audio_file)
                messages.success(request, "Audio uploaded successfully")
            else:
                messages.warning(request, "Please upload an MP3 file")
        else:
            messages.warning(request, "Form is invalid")
    else:
        form = AudioForm()
    return render(request, "audios/load_audio.html", {"form": form})


@csrf_exempt
def add_audio(request):
    if request.method == "POST":
        audio_id = request.POST.get("audioId")
        audio = Audio.objects.get(id=audio_id)
        if audio:
            if UserAudio.objects.filter(user=request.user, audio=audio).exists():
                return JsonResponse({"message": "You already added this track"})
            else:
                UserAudio.objects.create(audio=audio, user=request.user)
        else:
            return JsonResponse({"message": "Error"})
        return JsonResponse({"message": "You successfuly add this track"})
    else:
        return JsonResponse({"message": "Invalid method"}, status=405)
    
@csrf_exempt
def delete_audio(request):
    if request.method == "POST":
        audio_id = request.POST.get("audioId")
        try:
            audio = Audio.objects.get(pk=audio_id)
            user_audio = UserAudio.objects.get(user=request.user, audio=audio)
            user_audio.delete()
            return JsonResponse({"message": "You delete this track successfully"})
        except Audio.DoesNotExist:
            return JsonResponse({"message": "No such track in database"})
    else:
        return JsonResponse({"message": "Invalid method"})