import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import close_old_connections
from django.utils import timezone
from oauth2_provider.models import AccessToken


class RoomConsumer(AsyncWebsocketConsumer):
    access_token = None
    user = None
    group_name = None

    async def connect(self):
        # Extraer headers y token
        headers = dict((k.decode(), v.decode()) for k, v in self.scope["headers"])
        raw_token = headers.get("authorization", "").replace("Bearer ", "")

        # Validar el token usando el modelo de AccessToken
        try:
            close_old_connections()
            token_obj = await sync_to_async(AccessToken.objects.select_related("user").get)(token=raw_token)

            # Verificar expiración del token
            if token_obj.expires < timezone.now():
                await self.close(code=4003)
                return

            self.access_token = raw_token
            self.user = token_obj.user
            self.group_name = f"token_{self.access_token}"

        except AccessToken.DoesNotExist:
            await self.close(code=4003)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"WebSocket conectado con token válido. Usuario: {self.user}, grupo: {self.group_name}")

    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            print(f"Desconectado del grupo: {self.group_name}")

    async def enviarAlServer(self, event):
        await self.send(text_data=json.dumps({
            "data": event["data"]
        }))
