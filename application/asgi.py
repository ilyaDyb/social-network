"""
ASGI config for application project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.layers import get_channel_layer
from channels.security.websocket import AllowedHostsOriginValidator

import messanger.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                messanger.routing.websocket_urlpatterns
            )
        )
    ),
})

channel_layer = get_channel_layer()