from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task
from photocompetition.celery import app

channel_layer = get_channel_layer()

@shared_task
def send_notification():
    async_to_sync(channel_layer.group_send)('notifications', {'type': 'send_notification', 'text': "Work!"})

@app.task
def send_notice():
    async_to_sync(channel_layer.group_send)('notifications', {'type': 'send_notification', 'text': 'Work'})