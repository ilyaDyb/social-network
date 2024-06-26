"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from utilities.preview_view import preview_view
from . import settings
# from django.views.generic.base import RedirectView
from posts.utils import HomeRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include("posts.urls", namespace="posts")),
    path("", HomeRedirectView.as_view(url='/feed/'), name="home_redirect"),
    path("", include("users.urls", namespace="users")),
    path("", include("photos.urls", namespace="photos")),
    path("", include("audios.urls", namespace="audios")),
    path("apps/", include("apps.urls", namespace="apps")),
    path("messanger/", include("messanger.urls", namespace="messanger")),
    path("preview/<str:instance_type>/<int:instance_id>/", preview_view, name="preview"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
