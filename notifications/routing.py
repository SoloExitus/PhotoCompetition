from django.urls import path
from notifications.consumers import NotificationsConsumer, LikesConsumer

ws_urlpatterns = [
    path('ws/notifications/', NotificationsConsumer.as_asgi()),
    path('ws/likes/', LikesConsumer.as_asgi())
]