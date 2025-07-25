from django.urls import re_path

from ledsup import consumers

websocket_urlpatterns = [
    re_path(r'ledsup/wsremoteandlocal/$', consumers.RoomConsumer.as_asgi()),
    re_path('ws/estado/', consumers.EstadoConsumer.as_asgi()),
]
