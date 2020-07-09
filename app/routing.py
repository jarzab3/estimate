# chat/routing.py
from django.urls import re_path

from app import consumers

websocket_urlpatterns = [
    re_path(r'ws/'
            r'estimate/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]
