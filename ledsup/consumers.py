import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

@sync_to_async
def marcar_conectado(user_id):
    from .models import UserConnectionStatus
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    status, _ = UserConnectionStatus.objects.get_or_create(user=user)
    status.connected = True
    status.save()


@sync_to_async
def marcar_desconectado(user_id):
    from .models import UserConnectionStatus
    from django.contrib.auth.models import User
    try:
        user = User.objects.get(id=user_id)
        status = UserConnectionStatus.objects.get(user=user)
        status.connected = False
        status.save()
    except UserConnectionStatus.DoesNotExist:
        pass


class RoomConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.scope_user = None

    async def connect(self):
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
            # noinspection PyUnresolvedReferences
            await marcar_conectado(self.scope_user)
            # noinspection PyUnresolvedReferences
            await actualizar_ping(self.scope_user)
            await self.accept()
            print(f"WebSocket conectado: usuario {self.scope_user} agregado al grupo {self.group_name}")
            print(f"user_{self.scope_user}")
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                f"user_estado{self.scope_user}",
                {
                    "type": "estado_actualizado",
                    "data": {"estado": "conectado", "usuario": self.scope_user},
                }
            )

        except AccessToken.DoesNotExist:
            print("Token inválido o no encontrado")
            await self.close(code=4001)
        except Exception as e:
            print(f"Error en autenticación WebSocket: {e}")
            await self.close(code=4003)

    async def disconnect(self, close_code):
        if self.group_name:
            await marcar_desconectado(self.scope_user)
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            print(f"Desconectado del grupo {self.group_name}")

            await self.channel_layer.group_send(
                f"user_estado{self.scope_user}",
                {
                    "type": "estado_actualizado",
                    "data": {"estado": "desconectado", "usuario": self.scope_user},
                }
            )

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            if data.get("type") == "ping":
                await actualizar_ping(self.scope_user)
        except Exception as e:
            print(f"Error al procesar mensaje: {e}")

    async def kick_user(self, event):
        print(f"Usuario {self.scope_user} fue kickeado desde la web.")
        await self.close(code=4002)

    async def enviarAlServer(self, event):
        await self.send(text_data=json.dumps({
            "data": event["data"]
        }))

@sync_to_async
def actualizar_ping(user_id):
    from .models import UserConnectionStatus
    from django.contrib.auth.models import User
    from django.utils import timezone
    try:
        user = User.objects.get(id=user_id)
        status, _ = UserConnectionStatus.objects.get_or_create(user=user)
        status.lastPing = timezone.now()
        status.save()
    except User.DoesNotExist:
        pass

class EstadoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from .models import UserConnectionStatus
        from django.utils import timezone
        from datetime import timedelta

        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return

        self.user_group_name = f"user_estado{user.id}"
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()

        # Verifica el ping real del dispositivo
        status = await sync_to_async(UserConnectionStatus.objects.filter(user=user).first)()

        estado = "desconectado"
        if status:
            ahora = timezone.now()
            if status.connected and status.lastPing and ahora - status.lastPing < timedelta(seconds=30):
                estado = "conectado"

        await self.send(text_data=json.dumps({
            "estado": estado,
            "usuario": user.id,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def estado_actualizado(self, event):
        await self.send(text_data=json.dumps(event["data"]))
