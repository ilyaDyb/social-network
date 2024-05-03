from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Photo
from users.models import Users


def photos(request, username):
    try:
        user = Users.objects.get(username=username)
    except Users.DoesNotExist:
        return render(request, "photos/photos.html", context={"message": "User does not exist"})
    
    photos = user.photos.all().order_by("-id")
    context = {
        "photos": photos,
        "username": username,
    }
    return render(request, "photos/photos.html", context=context)


@login_required
@csrf_exempt
def load_photo(request):
    if request.method == "POST":
        image = request.FILES.get("file")
        index = str(image).rfind(".")
        
        if str(image)[index:] not in [".png", ".jpeg", "jpg", "webp"]:
            return JsonResponse({"message": "Invalid format"})
        
        if image.size > 10 * 1024 * 1024:
            return JsonResponse({"message": "Your file is too big"})
        try:
            Photo.objects.create(user=request.user, photo=image)
        except Exception as e:
            return JsonResponse({"message": e})
        return JsonResponse({"message": "Successfull"})

    else:
        return JsonResponse({"message": "Bad request"}, status=405)
    

@login_required
@csrf_exempt
def delete_photo(request):
    if request.method == "POST":
        photo_id = request.POST.get("photo_id")
        try:
            photo = Photo.objects.get(pk=photo_id)
            photo.delete()
            return JsonResponse({"message": "Success"}, status=200)
        except Photo.DoesNotExist:
            return JsonResponse({"message": "Does not exist"}, status=404)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)