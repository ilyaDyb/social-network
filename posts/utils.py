from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy


class HomeRedirectView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("feed")

    def get_redirect_url(self, *args, **kwargs) -> str | None:
        return super().get_redirect_url(*args, **kwargs)
    