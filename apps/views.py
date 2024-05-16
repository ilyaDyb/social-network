import http.client
import os
import http
import replicate
import requests
import random

from dotenv import load_dotenv
from fake_useragent import UserAgent

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index(request):
    # user = Users.objects.get(username="test1")
    # text = "Crocubot. So, you’re a cold, unfeeling reptile and also an equally cold, and unfeeling machine? Yes. So your origin is what? You fell in a vat of redundancy?"

    # for i in range(1, 4):
    #     Post.objects.create(user=user, text=text, image=f"post_images/example{i}.webp")
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
            },
        )
        return JsonResponse(
            {"message": "success", "image": output}, status=http.client.OK
        )
    else:
        return JsonResponse({"message": "Bad request"}, status=http.client.BAD_REQUEST)


def avatar_rick_and_morty(request):
    return render(request, "apps/generate_avatar_rick_and_morty.html")


@csrf_exempt
def avatar_rick_and_morty_generate(request):
    if request.method == "POST":
        try:
            page = random.randint(0, 42)
            url = f"https://rickandmortyapi.com/api/character?page={page}"
            headers = {"user-agent": str(UserAgent.random)}
            response = requests.get(url=url, headers=headers, timeout=60).json()
            characters = random.randint(0, len(response["results"]) - 1)
            character = response["results"][int(characters)]

            data = {
                "name": character["name"],
                "status": character["status"],
                "species": character["species"],
                "gender": character["gender"],
                "src": character["image"],
                "message": "Success",
            }
            return JsonResponse(data, status=http.client.OK)
        except Exception as ex_:
            return JsonResponse(
                {"message": ex_}, status=http.client.INTERNAL_SERVER_ERROR
            )
    else:
        return JsonResponse({"message": "Bad request"}, status=http.client.BAD_REQUEST)
