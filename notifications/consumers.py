import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from competition.models import User, PhotoPost


class NotificationsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add('notifications', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard('notifications', self.channel_name)
        await super().disconnect(code)

    async def send_notification(self, event):
        text = event['text']

        await self.send(text)
        #await self.send(json.dumps(notification_text))


class LikesConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(f'{self.user.id}', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(f'{self.user.id}', self.channel_name)

        await super().disconnect(code)

    async def like_notification(self, event):
        userId = event['userId']
        postId = event['postId']
        user_info = await get_user_info(userId)
        post_info = await get_post_info(postId)
        data = user_info | post_info
        await self.send(json.dumps(data))



@database_sync_to_async
def get_post_info(postId):
    post = PhotoPost.objects.get(id=postId)
    return {'post_title': post.title, 'post_preview_image': post.preview_image.url}

@database_sync_to_async
def get_user_info(userId):
    user = User.objects.get(id=userId)
    return {'username': user.username, 'user_profile_image': user.profile_image}