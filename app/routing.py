# chat/routing.py
from django.conf.urls import re_path
from app import consumers

websocket_urlpatterns = [
    re_path(r'agile/ws/'
            r'estimate/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]
