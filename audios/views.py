from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin

from audios.services import AudioService, UserAudioService

from .models import Audio, UserAudio
from .forms import AudioForm

class LoginRequiredView(View, LoginRequiredMixin):
    pass


class AudioRedirectView(LoginRequiredView):
    def get(self, request):
        redirect_url = f"/audios/{request.user.username}/"
        return redirect(redirect_url)
    

class AudioListView(LoginRequiredView):
    template_name = "audios/audios.html"

    def get(self, request, username=None):
        if not username:
            return redirect(f"/audios/{request.user.username}/")
        search = request.GET.get("search")
        audios, flag = AudioService.get_audio_for_user(username, search)

        if audios is None:
            return HttpResponse(status=404)
        context = {
            "username": username,
            "audios": audios.order_by("-id"),
            #"audios": sorted(audios, key=lambda x: x.id, reverse=True)
            "flag": flag,
        }
        return render(request, self.template_name, context=context)

class LoadAudio(LoginRequiredView):
    template_name = "audios/load_audio.html"
    
    def get(self, request):
        form = AudioForm()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        audio, msg = AudioService.load_audio(request)
        if not audio:
            messages.warning(request, msg)   
        else:
            messages.success(request, msg)
        return render(request, self.template_name, {"form": AudioForm()})


@method_decorator(csrf_exempt, "dispatch")
class AddAudio(LoginRequiredView):
    def post(self, request):
        msg  = UserAudioService.add_audio(request)
        return JsonResponse({"message":msg})
        

@csrf_exempt
def delete_audio(request):
    if request.method == "POST":
        audio_id = request.POST.get("audioId")
        try:
            audio = Audio.objects.get(pk=audio_id)
            UserAudio.objects.get(user=request.user, audio=audio)
            return JsonResponse({"message": "You delete this track successfully"})
        except Audio.DoesNotExist:
            return JsonResponse({"message": "No such track in database"})
    else:
        return JsonResponse({"message": "Invalid method"})

@method_decorator(csrf_exempt, "dispatch")
class DeleteAudio(LoginRequiredView):
    def post(self, request):
        msg = UserAudioService.delete_audio_for_user(request)
        return JsonResponse({"message": msg})

def preview(request, audio_id):
    try:
        audio = Audio.objects.get(pk=audio_id)
        return render(request, "base_preview_page.html", context={"audio": audio})
    except Audio.DoesNotExist:
        return HttpResponse(404)