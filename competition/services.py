from django.contrib.auth import get_user_model
from service_objects.services import Service
from .models import Like


def like_post(post, user):
    if user.id == post.user.id or not user.is_authenticated:
        return

    like, is_created = Like.objects.get_or_create(post=post, user=user)


def unlike_post(post, user):
    Like.objects.get(post=post, user=user).delete()


def is_liked_post(post, user) -> bool:
    if not user.is_authenticated:
        return False

    likes = Like.objects.filter(post=post, user=user)
    return likes.exists()

