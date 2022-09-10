from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task
from photocompetition.celery import app

channel_layer = get_channel_layer()

@shared_task
def send_notification_everyone(text):
    async_to_sync(channel_layer.group_send)('notifications', {'type': 'send_notification', 'text': text})

@app.task
def send_like_notification(who_like_id, post_id, user_id):
    async_to_sync(channel_layer.group_send)(f'{user_id}', {'type': 'like_notification',
                                                           'userId': who_like_id, 'postId': post_id})