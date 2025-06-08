import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtener token de headers
        headers = dict((k.decode(), v.decode()) for k, v in self.scope["headers"])
        token = headers.get("authorization", "").replace("Token ", "")

        # Validar token
        if token != settings.WS_SECRET_TOKEN:
            await self.close(code=4003)
            return

        await self.channel_layer.group_add("pc_apps", self.channel_name)
        await self.accept()
        print("WebSocket conectado y agregado a grupo pc_apps")

    async def disconnect(self, close_code):
        print("Desconectado")
        await self.channel_layer.group_discard("pc_apps", self.channel_name)

    async def enviarAlServer(self, event):
        await self.send(text_data=json.dumps({
            "data": event["data"]
        }))
