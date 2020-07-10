from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    # path('', views.chat_view, name='chat_view'),
    path('<str:room_name>/<str:name>', views.estimate_view, name='room'),
    # url('<str:room_name>/<str:name>', views.estimate_view, name="room"),
]
