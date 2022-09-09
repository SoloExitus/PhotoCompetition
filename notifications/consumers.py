import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add('notifications', self.channel_name)
        await self.accept()

        # for i in range(500):
        #     await self.send(json.dumps({'message': i}))

    async def disconnect(self, code):
        await self.channel_layer.group_discard('notifications', self.channel_name)
        await super().disconnect(code)

    async def send_notification(self, event):
        text = event['text']

        await self.send(text)
        #await self.send(json.dumps(notification_text))