from django.urls import path
from notifications.consumers import NotificationsConsumer

ws_urlpatterns = [
    path('ws/notifications/', NotificationsConsumer.as_asgi())
]