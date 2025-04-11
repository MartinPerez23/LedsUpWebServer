import json

from channels.generic.websocket import AsyncWebsocketConsumer

from django.conf import settings


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtenés el token desde la cabecera
        headers = dict((k.decode(), v.decode()) for k, v in self.scope["headers"])
        token = headers.get("authorization", "").replace("Token ", "")

        # Comparás con un token definido en tus settings
        if token != settings.WS_SECRET_TOKEN:
            await self.close(code=4003)  # 4003 = código de cierre personalizado
            return

        await self.accept()

    async def disconnect(self, close_code):
        print("Desconectado")

    async def enviarAlServer(self, datosAEnviar):
        await self.send(text_data=json.dumps(datosAEnviar))
