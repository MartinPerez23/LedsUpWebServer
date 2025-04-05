import json

from channels.generic.websocket import AsyncWebsocketConsumer


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Nueva app conectada desde la PC")
        await self.channel_layer.group_add("pc_apps", self.channel_name)

    async def disconnect(self, close_code):
        print("Desconectado")

    async def enviarAlServer(self, datosAEnviar):
        await self.send(text_data=json.dumps(datosAEnviar))
