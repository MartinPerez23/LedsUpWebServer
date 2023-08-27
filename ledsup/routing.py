from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
        #path('ledsup/wsremoteandlocal/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
        re_path(r"ws/ledsup/wsremoteandlocal/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
