import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mini_slack.settings.dev")

# Module 12+ will replace this with a ProtocolTypeRouter that adds a
# Channels websocket URLRouter alongside this http application.
application = get_asgi_application()
