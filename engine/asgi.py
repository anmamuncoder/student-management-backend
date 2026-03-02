"""
ASGI config for engine project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Import Channels components for WebSocket support
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'engine.settings')

django_asgi_app  = get_asgi_application()
# django_wsgi_app = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app ,
#         "websocket": AuthMiddlewareStack(URLRouter(chat_ws.websocket_urlpatterns)),
#     }
# )
application = django_asgi_app

