import http.client
import os
import replicate
import http
from dotenv import load_dotenv

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "apps/index.html")


def ai_images(request):
    return render(request, "apps/ai_images.html")

@csrf_exempt
def generate_image(request):
    if request.method == "POST":

        prompt = request.POST.get("prompt")
        load_dotenv()
        REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
        api = replicate.Client(api_token=REPLICATE_API_TOKEN)

        output = api.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={
                "width": 704,
                "height": 512,
                "prompt": prompt,
            }
        )
        return JsonResponse({"message": "success", "image": output}, status=http.client.OK)
    else:
        return JsonResponse({"message": "Bad request"}, status=400)