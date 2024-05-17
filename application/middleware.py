from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils import timezone

class SpamProtectionMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.cache_timeout = 300
        self.request_limit = 12
        self.block_period = 48

    def __call__(self, request):
        if request.path.startswith("/static/") or request.path.startswith("/media/"):
            return self.get_response(request)
        
        ip_address = self.get_client_ip(request)

        if not ip_address:
            return HttpResponseForbidden("IP address not found")
        
        cache_key = f"spam_from_{ip_address}"
        current_time = timezone.now()

        spam_object = cache.get(key=cache_key)

        if spam_object:
            request_times, first_request_time = spam_object
            if (current_time - first_request_time).total_seconds() < self.block_period:
                if len(request_times) >= self.request_limit:
                    return HttpResponseForbidden("Too many requests")
                else:
                    request_times.append(current_time)
            else:
                request_times = [current_time]
                first_request_time = current_time
        else:
            request_times = [current_time]
            first_request_time = current_time
        cache.set(cache_key, (request_times, first_request_time), self.cache_timeout)
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("X-Forwarded-For")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip