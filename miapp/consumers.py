import json
from channels.generic.websocket import AsyncWebsocketConsumer
import random
import asyncio
from channels.db import database_sync_to_async

class RuletaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("ruleta", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("ruleta", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('action') == 'spin':
            is_admin = await database_sync_to_async(self._is_admin)()
            if is_admin:
                vendidos = await database_sync_to_async(self._get_vendidos)()
                await self.channel_layer.group_send(
                    "ruleta",
                    {
                        "type": "ruleta_start_animation",
                        "vendidos": vendidos,
                    }
                )
                await asyncio.sleep(10)
                if vendidos:
                    resultado = random.choice(vendidos)
                else:
                    resultado = "Sin números vendidos"
                await self.channel_layer.group_send(
                    "ruleta",
                    {
                        "type": "ruleta_resultado",
                        "resultado": resultado,
                    }
                )

    def _is_admin(self):
        user = self.scope.get("user", None)
        return user and user.is_authenticated and user.is_superuser

    def _get_vendidos(self):
        from miapp.models import Numero
        return list(Numero.objects.filter(disponible=False).values_list('valor', flat=True))

    async def ruleta_start_animation(self, event):
        await self.send(text_data=json.dumps({
            "action": "start_animation",
            "vendidos": event["vendidos"]
        }))

    async def ruleta_resultado(self, event):
        await self.send(text_data=json.dumps({
            "action": "stop_animation",
            "resultado": event["resultado"]
        }))