from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from audios.models import Audio
from photos.models import Photo
from posts.models import Post


def preview_view(request, instance_type, instance_id):
    if request.user.is_staff:
        if instance_type == "audio":
            instance = get_object_or_404(Audio, pk=instance_id)
        elif instance_type == "post":
            instance = get_object_or_404(Post, pk=instance_id)
        elif instance_type == "photo":
            instance = get_object_or_404(Photo, pk=instance_id)
        else:
            return HttpResponse(status=404)
        return render(request, "base_preview_page.html", context={instance_type: instance})
    else:
        return HttpResponse(status=404)