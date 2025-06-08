import json
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class RoomConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.scope_user = None

    async def connect(self):
        # Importar aquí para evitar el error de AppRegistryNotReady
        from oauth2_provider.models import AccessToken

        headers = dict((k.decode(), v.decode()) for k, v in self.scope["headers"])
        token = headers.get("authorization", "").replace("Bearer ", "").strip()

        try:
            access_token = await sync_to_async(AccessToken.objects.select_related("user").get)(token=token)

            is_expired = await sync_to_async(access_token.is_expired)()
            if is_expired:
                raise Exception("Token expirado")

            self.scope_user = access_token.user.id
            self.group_name = f"user_{self.scope_user}"

            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            print(f"WebSocket conectado: usuario {self.scope_user} agregado al grupo {self.group_name}")

        except AccessToken.DoesNotExist:
            print("Token inválido o no encontrado")
            await self.close(code=4003)
        except Exception as e:
            print(f"Error en autenticación WebSocket: {e}")
            await self.close(code=4003)

    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            print(f"Desconectado del grupo {self.group_name}")

    async def enviarAlServer(self, event):
        await self.send(text_data=json.dumps({
            "data": event["data"]
        }))
